from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Milvus
from langchain.chains import RetrievalQA


class LangChainService:
    """
    通用的 LangChain 服务，用于直接调用 LLM 模型。
    """
    def __init__(self):
        # 初始化 LLM 模型
        self.llm = ChatOpenAI(
            model='deepseek-chat', 
            openai_api_key='sk-764e5f5acea340ea816a014d1503f749', 
            openai_api_base='https://api.deepseek.com',
            max_tokens=1024
        )

    def get_response(self, prompt: str) -> str:
        """
        调用 LLM 模型并返回响应内容
        :param prompt: 输入的提示文本
        :return: 模型生成的响应内容
        """
        response = self.llm.invoke(prompt)
        return response.content


class PDFKnowledgeBase:
    """
    基于 PDF 文档的知识库，支持加载 PDF 并回答问题。
    """
    def __init__(self, pdf_path: str, milvus_host: str = "localhost", milvus_port: str = "19530"):
        """
        初始化 PDF 知识库
        :param pdf_path: PDF 文件路径
        :param milvus_host: Milvus 服务器地址
        :param milvus_port: Milvus 服务器端口
        """
        self.pdf_path = pdf_path
        self.embeddings = OpenAIEmbeddings()  # 使用 OpenAI 嵌入模型
        self.llm = ChatOpenAI(
            model='deepseek-chat',
            openai_api_key='sk-764e5f5acea340ea816a014d1503f749',
            openai_api_base='https://api.deepseek.com',
            max_tokens=1024
        )
        self.milvus_host = milvus_host
        self.milvus_port = milvus_port
        self.vector_store = None
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """
        加载 PDF 文档，分割并嵌入到 Milvus 向量数据库中
        """
        # 加载 PDF 文档
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()

        # 分割文档
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # 每个块的大小
            chunk_overlap=200  # 块之间的重叠部分
        )
        chunks = text_splitter.split_documents(documents)

        # 嵌入并存储到 Milvus 向量数据库
        self.vector_store = Milvus.from_documents(
            chunks,
            self.embeddings,
            connection_args={"host": self.milvus_host, "port": self.milvus_port},
            collection_name="pdf_knowledge_base"  # Milvus 集合名称
        )

    def ask_question(self, question: str) -> str:
        """
        基于知识库回答问题
        :param question: 用户提问
        :return: 模型生成的回答
        """
        # 创建检索链
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )

        # 获取回答
        response = qa_chain.invoke({"query": question})
        return response["result"]


# 示例用法
# if __name__ == "__main__":
#     # 初始化 PDF 知识库
#     pdf_kb = PDFKnowledgeBase("example.pdf", milvus_host="localhost", milvus_port="19530")

#     # 提问
#     question = "What is the main topic of this document?"
#     answer = pdf_kb.ask_question(question)
#     print(f"Question: {question}")
#     print(f"Answer: {answer}")