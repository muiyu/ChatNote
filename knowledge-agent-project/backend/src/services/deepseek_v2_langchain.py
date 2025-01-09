import markdown
import re
import os
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings

if "OPENAI_API_KEY" not in os.environ:
    api_key = getpass.getpass("OpenAI API Key:")
else:
    api_key = os.environ["OPENAI_API_KEY"]

if "OPENAI_BASE_URL" not in os.environ:
    api_base = getpass.getpass("OpenAI Base URL:")
else:
    api_base = os.environ["OPENAI_BASE_URL"]

class LangChainService:
    def __init__(self, question, markdown_content=None):
        """
        初始化 LangChainService。
        :param question: 问题
        :param markdown_content: Markdown 内容（可选）
        """
        self.markdown_content = markdown_content  # Markdown 内容（可选）
        self.question = question  # 问题
        self.llm = ChatOpenAI(
            model='gpt-4o',
            openai_api_key=api_key,
            openai_api_base=api_base,
            max_tokens=1024
        )
        self.embeddings = OpenAIEmbeddings()

    def markdown_to_text(self):
        """
        将 Markdown 内容转换为纯文本。
        """
        if not self.markdown_content:
            return ""  # 如果没有 Markdown 内容，返回空字符串

        html_content = markdown.markdown(self.markdown_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        plain_text = soup.get_text()
        plain_text = re.sub(r'\n\s*\n', '\n\n', plain_text).strip()
        return plain_text

    def create_vectorstore(self):
        """
        创建向量存储。
        """
        if not self.markdown_content:
            return None  # 如果没有 Markdown 内容，返回 None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)
        chunks = text_splitter.split_text(self.markdown_to_text())
        documents = [Document(page_content=chunk) for chunk in chunks]
        vectorstore = FAISS.from_documents(documents[:5], embedding=self.embeddings)
        return vectorstore.as_retriever()

    def build_chain(self, retriever=None):
        """
        构建处理链。
        :param retriever: 向量存储的检索器（可选）
        """
        if retriever:
            # 如果有向量存储，使用上下文回答问题
            template = """Answer the question based only on the following context:
            {context}

            Question: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)
            chain = (
                {
                    "context": retriever,
                    "question": RunnablePassthrough()
                }
                | prompt
                | self.llm
                | StrOutputParser()
            )
        else:
            # 如果没有向量存储，直接回答问题
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

    def process_query(self):
        """
        处理查询。
        """
        retriever = self.create_vectorstore()  # 创建向量存储（如果有 Markdown 内容）
        chain = self.build_chain(retriever)  # 构建处理链
        response = chain.invoke(self.question)  # 调用处理链
        print(response)  # 打印响应
        return response