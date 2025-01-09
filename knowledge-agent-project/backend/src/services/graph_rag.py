import os
import getpass
import re
import markdown
import time
from bs4 import BeautifulSoup

from typing import List, Optional

# ---- Neo4j 相关 ----
from langchain_neo4j import Neo4jVector, Neo4jGraph
# 假设这里您已经有 parse_markdown、GraphIniter 或者类似函数/类，可以直接复用
# 如果想在这个类里内置 Markdown -> Neo4j 存储的逻辑，则可引入我们之前写的 parse_markdown 等函数。

# ---- LangChain 相关 ----
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document  # 注意：根据您的实际环境决定导入路径
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class MDHeadingNode:
    """
    读取 MD 内容时的抽象节点类

    用于表示读取过程中的 MD 结构，包括：
    - heading_level: 标题级别（1~5）
    - title: 标题文本（不含 #）
    - text: 标题文本 + 正文内容（对于 H2-H5 的 chunk 节点要使用；若为 H1 则忽略正文）
    - parent: 父节点
    - children: 子节点列表
    """
    def __init__(self, heading_level: int, title: str):
        self.heading_level = heading_level
        self.title = title.strip()
        self.text = self.title                                      # text 初始值先设置为标题文本，后续正文会追加
        self.parent: Optional['MDHeadingNode'] = None
        self.children: List['MDHeadingNode'] = []

    def add_child(self, child: 'MDHeadingNode'):
        child.parent = self
        self.children.append(child)

    def add_text(self, more_text: str):
        """将正文内容拼接到 text 属性上；若是空行则忽略。"""
        if more_text.strip():
            self.text += "\n" + more_text.strip()


class GraphIniter:
    """
    GraphIniter 类
    
    1. 解析 Markdown 内容并将其存储到 Neo4j 图数据库中。
    2. 初始化时会自动构建图数据库。
    3. 提供 rebuild 方法以删除当前数据库内容并重新构建图。
    """

    def __init__(self, md_content: str):
        self.md_content = md_content 
        self.url = self._get_env_or_prompt("NEO4J_URI", "Neo4j URI:")
        self.username = self._get_env_or_prompt("NEO4J_USERNAME", "Neo4j Username:")
        self.password = self._get_env_or_prompt("NEO4J_PASSWORD", "Neo4j Password:")
        self.graph = Neo4jGraph(
            url=self.url,
            username=self.username,
            password=self.password
        )
        self.root_nodes = self.parse_markdown(self.md_content)                                              # 解析 Markdown 内容
        self.clear_graph_database()
        self.store_knowledge_graph(self.root_nodes)                                                         # 构建图数据库

    def _get_env_or_prompt(self, var_name: str, prompt_text: str) -> str:
        """
        获取环境变量，如果不存在则提示用户输入。
        """
        if var_name not in os.environ:
            return getpass.getpass(prompt_text)
        else:
            return os.environ[var_name]

    def parse_markdown(self, md_text: str) -> List[MDHeadingNode]:
        """
        解析 Markdown 文本，匹配 1~5 级标题 (#, ##, ###, ####, #####)。
        超过 5 级的标题将被忽略或视为普通文本。
        返回可能存在多个根节点（多个 H1）组成的列表。
        """
        lines = md_text.split("\n")
        heading_pattern = re.compile(r'^(#{1,5})\s+(.*)$')

        root_nodes: List[MDHeadingNode] = []
        stack: List[MDHeadingNode] = []

        for line in lines:
            line = line.rstrip()
            match = heading_pattern.match(line)

            if match:
                # 匹配到标题行
                hashes = match.group(1)
                title_text = match.group(2)
                level = len(hashes)  # 标题层级 1~5

                if level > 5:
                    # 忽略超过5级的标题
                    continue

                new_node = MDHeadingNode(heading_level=level, title=title_text)

                if not stack:
                    # 空栈，直接作为新的根节点
                    root_nodes.append(new_node)
                    stack.append(new_node)
                else:
                    # 栈不为空，需要根据层级调整栈顶
                    while stack and stack[-1].heading_level >= level:
                        stack.pop()

                    if not stack:
                        # 这是一个新的根节点
                        root_nodes.append(new_node)
                        stack.append(new_node)
                    else:
                        # 当前节点是栈顶节点的子节点
                        stack[-1].add_child(new_node)
                        stack.append(new_node)
            else:
                # 非标题行，视为正文，追加到当前栈顶节点
                if stack:
                    stack[-1].add_text(line)

        return root_nodes

    def match_course_node_query(self, title: str) -> str:
        """
        在数据库中查找同名的 course 节点，并返回其 id。
        """
        return \
        f"""
        MATCH (c:course {{ title: "{title.replace('"', '\\"')}" }})
        RETURN id(c) AS node_id
        """

    def create_course_node_query(self, title: str) -> str:
        """
        创建一个新的 course 节点，仅包含 title 属性。
        """
        return \
        f"""
        CREATE (c:course {{
            title: "{title.replace('"', '\\"')}"
        }})
        RETURN id(c) AS node_id
        """

    def create_chunk_node_query(self, title: str, text: str, level: str) -> str:
        """
        创建一个新的 chunk 节点，包含 title、text、level 三个属性。
        例如 level = "h2"|"h3"|"h4"|"h5"。
        """
        return \
        f"""
        CREATE (ck:chunk {{
            title: "{title.replace('"', '\\"')}",
            text: "{text.replace('"', '\\"')}",
            level: "{level}"
        }})
        RETURN id(ck) AS node_id
        """

    def create_relationship_query(self, parent_id: int, child_id: int) -> str:
        """
        为已有的两个节点创建 :CHILD 关系。
        因为没有强制要求按照 label 匹配，所以这里只用 id() 即可。
        """
        return \
        f"""
        MATCH (p), (c)
        WHERE id(p) = {parent_id} AND id(c) = {child_id}
        CREATE (p)-[:CHILD]->(c)
        """

    def store_knowledge_graph(self, root_nodes: List[MDHeadingNode]):
        """
        将解析后的节点存储到 Neo4j 图数据库中。

        - heading_level == 1 → course 节点（复用 / 新建）
          - 不存 text，不存 level
        - heading_level in [2..5] → chunk 节点（每次新建）
          - 存 title、text、level (如 "h2"/"h3"/"h4"/"h5")
        """

        def traverse_and_store(node: MDHeadingNode, parent_id: Optional[int] = None):
            node_id = None

            if node.heading_level == 1:
                # 处理 course 节点（H1），复用或新建
                query_match = self.match_course_node_query(node.title)
                match_result = self.graph.query(query_match)

                if match_result and len(match_result) > 0 and match_result[0].get("node_id") is not None:
                    # 已存在同名的 course 节点
                    node_id = match_result[0]["node_id"]
                else:
                    # 不存在，则创建新的 course
                    query_create = self.create_course_node_query(node.title)
                    create_result = self.graph.query(query_create)
                    node_id = create_result[0]["node_id"]

            else:
                # 处理 chunk 节点（H2-H5），直接新建
                level_str = f"h{node.heading_level}"  # "h2", "h3", "h4", "h5"
                query_create = self.create_chunk_node_query(node.title, node.text, level_str)
                create_result = self.graph.query(query_create)
                node_id = create_result[0]["node_id"]

            # 如果有父节点，则创建父子关系
            if parent_id is not None:
                rel_query = self.create_relationship_query(parent_id, node_id)
                self.graph.query(rel_query)

            # 递归处理子节点
            for child in node.children:
                traverse_and_store(child, node_id)

        # 遍历每一个根节点
        for root_node in root_nodes:
            traverse_and_store(root_node, None)

    def clear_graph_database(self):
        """
        清空图数据库中的所有内容，包括节点、关系、约束和索引。
        使用 SHOW INDEXES 和 SHOW CONSTRAINTS 来获取并删除所有索引和约束。
        """

        try:
            # 删除所有关系和节点
            delete_all_query = "MATCH (n) DETACH DELETE n"
            self.graph.query(delete_all_query)
            print("所有节点和关系已删除。")
        except Exception as e:
            print(f"删除节点和关系时出错: {e}")

        try:
            # 删除所有约束
            show_constraints_query = "SHOW CONSTRAINTS"
            constraints = self.graph.query(show_constraints_query)
            for constraint in constraints:
                constraint_name = constraint.get("name")
                if constraint_name:
                    drop_constraint_query = f"DROP CONSTRAINT {constraint_name}"
                    self.graph.query(drop_constraint_query)
                    print(f"已删除约束: {constraint_name}")
        except Exception as e:
            print(f"删除约束时出错: {e}")

        try:
            # 删除所有索引
            show_indexes_query = "SHOW INDEXES"
            indexes = self.graph.query(show_indexes_query)
            for index in indexes:
                index_name = index.get("name")
                if index_name:
                    drop_index_query = f"DROP INDEX {index_name}"
                    self.graph.query(drop_index_query)
                    print(f"已删除索引: {index_name}")
        except Exception as e:
            print(f"删除索引时出错: {e}")

    def rebuild(self):
        """
        删除当前图数据库的所有内容并重新构建图。
        """
        self.clear_graph_database()
        self.store_knowledge_graph(self.root_nodes)


class GraphRAGService:
    """
    GraphRAGService 用于：
    1. （可选）把给定的 Markdown 内容解析并存入 Neo4j 图数据库；
    2. 从 Neo4j 图数据库里做相似度检索，获取相关节点的上下文；
    3. 调用 LLM，基于问题 + 检索到的上下文，生成回答。
    
    使用示例：
        rag_service = GraphRAGService(
            question="请简要说说 GFS？",
            markdown_content="..."  # 可选，若不传则只进行检索
        )
        answer = rag_service.process_query()
        print(answer)
    """

    def __init__(self, question: str, markdown_content: str = None):
        """
        初始化 GraphRAGService
        :param question: 用户问题
        :param markdown_content: 可选的 Markdown 内容
        """
        self.question = question
        self.markdown_content = markdown_content
        
        # 处理 OpenAI 的 API Key & Base URL
        if "OPENAI_API_KEY" not in os.environ:
            os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
        if "OPENAI_BASE_URL" not in os.environ:
            os.environ["OPENAI_BASE_URL"] = getpass.getpass("OpenAI Base URL:")

        self.api_key = os.environ["OPENAI_API_KEY"]
        self.api_base = os.environ["OPENAI_BASE_URL"]

        # 处理 Neo4j 的连接参数
        if "NEO4J_URI" not in os.environ:
            self.url = getpass.getpass("Neo4j URI:")
        else:
            self.url = os.environ["NEO4J_URI"]

        if "NEO4J_USERNAME" not in os.environ:
            self.username = getpass.getpass("Neo4j Username:")
        else:
            self.username = os.environ["NEO4J_USERNAME"]

        if "NEO4J_PASSWORD" not in os.environ:
            self.password = getpass.getpass("Neo4j Password:")
        else:
            self.password = os.environ["NEO4J_PASSWORD"]

        # 初始化 ChatOpenAI
        self.llm = ChatOpenAI(
            model='gpt-4o',
            openai_api_key=self.api_key,
            openai_api_base=self.api_base,
            max_tokens=1024
        )
        self.embeddings = OpenAIEmbeddings()

        # 如果传入 markdown_content，则可选地做一次图构建
        # 如果您已有图可用，也可以不在这里做，而是独立的过程。
        if self.markdown_content:
            self._store_markdown_in_graph(self.markdown_content)

        # 初始化或者连接已存在的 Neo4jVector
        # 假设图中已经有 label=chunk、property=text、embedding=embedding 的向量索引
        self.db = Neo4jVector.from_existing_graph(
            embedding=self.embeddings,
            url=self.url,
            username=self.username,
            password=self.password,
            index_name="vector",  # 建立向量索引的名称
            node_label="chunk",
            text_node_properties=["title"],
            embedding_node_property="embedding"
        )

        #time.sleep(5)

    # -------------------------------------------------------------------------
    # 可选：把 Markdown 存到图数据库
    # 若您已经有 GraphIniter 或类似代码，可在此直接调用
    # -------------------------------------------------------------------------
    def _store_markdown_in_graph(self, md_content):
        """
        将当前的 self.markdown_content 解析并存储到 Neo4j 图数据库。
        这里仅示范最简要的流程，如需更复杂的标题/层级结构处理，
        可引入我们之前写的 parse_markdown / store_knowledge_graph 等函数。
        """
        graph_initer = GraphIniter(md_content)

    # -------------------------------------------------------------------------
    # 下面是根据第二份示例代码改写的检索逻辑
    # -------------------------------------------------------------------------
    def _init_node_search(self, query: str) -> str:
        """
        取得最初最相似的一段 text（对应某一个 chunk 节点的 text）
        """
        results = self.db.similarity_search_with_score(query, k=1)
        if not results:
            return ""
        doc, _ = results[0]
        # doc.page_content 会是类似 "text: xxxx"
        # 若您创建 chunk 节点时并未添加 "text: " 前缀，则无需 lstrip
        print(doc.page_content.lstrip("\ntitle: "))
        return doc.page_content.lstrip("\ntitle: ")

    def _get_chunk_and_children_including_self(self, text_value: str):
        """
        根据给定的 text_value, 找到对应 chunk 节点；
        并在同一条查询中，递归查找自身及所有子节点的 text。
        """
        # 直接使用当前的 Neo4jVector 对象获取 graph
        graph = self.db

        query = f'''
        MATCH (c:chunk {{title: "{text_value.replace('"', '\\"')}"}})
        OPTIONAL MATCH (c)-[:CHILD*0..]->(descendant:chunk)
        RETURN
          id(c) AS chunkId,
          c.title AS chunkTitle,
          c.text AS chunkText,
          c.level AS chunkLevel,
          collect(distinct descendant.text) AS childTexts
        '''
        result = graph.query(query)
        if not result or len(result) == 0:
            return None
        record = result[0]
        chunk_info = {
            "chunkId": record["chunkId"],
            "title": record["chunkTitle"],
            "text": record["chunkText"],
            "level": record["chunkLevel"],
            "childTexts": record["childTexts"]  # list[str]
        }
        return chunk_info

    def _build_context_from_graph(self, query: str) -> str:
        """
        1. 相似度检索找到最相近的 chunk.text
        2. 根据 chunk.text 找到该节点 + 子节点文本
        3. 拼成最终的上下文字符串
        """
        text_value = self._init_node_search(query)
        if not text_value:
            return ""

        chunk_info = self._get_chunk_and_children_including_self(text_value)
        if not chunk_info:
            return ""

        # 拼装上下文：自身 + 所有子节点
        lines = []
        # 由于 childTexts 包含了自身 text，所以只要把 childTexts 展开即可
        for t in chunk_info["childTexts"]:
            if t.strip():
                lines.append(t.strip())
        context_str = "\n\n".join(lines)
        print(context_str)
        return context_str

    # -------------------------------------------------------------------------
    # 构建 LLM Chain，并生成答案
    # -------------------------------------------------------------------------
    def _build_chain(self, context_str: str):
        """
        构建一个简易的 LangChain 流水线：
        1) prompt + context
        2) ChatOpenAI
        3) 输出解析
        """
        if context_str:
            template = """Answer the question based only on the following context:
            {context}

            Question: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)
            chain = (
                {
                    "context": RunnablePassthrough(),
                    "question": RunnablePassthrough()
                }
                | prompt
                | self.llm
                | StrOutputParser()
            )
            return chain
        else:
            # 如果检索不到上下文，就直接回答
            template = """Answer the following question:
            Question: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)
            chain = (
                {"question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            return chain

    def process_query(self) -> str:
        """
        处理查询：
         1. 先在图中检索上下文；
         2. 构建 LLM chain；
         3. 调用 chain 生成答案；
         4. 返回答案字符串
        """
        # 1. 从图中检索上下文
        context_str = self._build_context_from_graph(self.question)

        # 2. 构建处理链
        chain = self._build_chain(context_str)

        # 3. 调用处理链，得到答案
        inputs = {
            "context": context_str,
            "question": self.question
        }
        answer = chain.invoke(inputs)
        print(answer)

        # 4. 返回答案
        return answer


# ------------------------------------------------------------------------------
# 使用示例
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    """
    假设已经有部分数据存入 Neo4j 图数据库中，或者您传入了新的 markdown_content。
    这里仅演示基本用法。
    """
    # 读取 MD 文件
    with open("./notes/note-2.md", "r", encoding="utf-8") as f:
        md_content = f.read()

    service = GraphRAGService(
        question="你能介绍一下太阳系的行星吗？",
        markdown_content=md_content  # 如果已经构建好图，可以不传
    )
    response = service.process_query()
    print("---- 最终回答 ----")
    print(response)
