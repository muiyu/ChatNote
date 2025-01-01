# pip3 install langchain_openai
# python3 deepseek_v2_langchain.py
import markdown
from bs4 import BeautifulSoup
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
def markdown_to_text(markdown_file):
    """
    将 Markdown 文件转换为纯文本。

    :param markdown_file: Markdown 文件的路径
    :return: 纯文本内容
    """
    # 读取 Markdown 文件
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    # 将 Markdown 转换为 HTML
    html_content = markdown.markdown(markdown_content)

    # 使用 BeautifulSoup 提取纯文本
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text()

    plain_text = re.sub(r'\n\s*\n', '\n\n', plain_text)  # 将连续的空行替换为单个空行
    plain_text = plain_text.strip() 

    return plain_text

llm = ChatOpenAI(
    model='deepseek-chat', 
    openai_api_key='sk-764e5f5acea340ea816a014d1503f749', 
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

# response = llm.invoke("Hi!")
# print(response.content)

markdown_file = "example.md"  # 替换为你的 Markdown 文件路径
plain_text = markdown_to_text(markdown_file)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = text_splitter.split_text(plain_text)
# print(chunks)
# print("-------------------------------------------------")
documents = [Document(page_content=chunk) for chunk in chunks]
# print(documents)

local_embeddings = OllamaEmbeddings(model="llama2-chinese:13b")
vectorstore = FAISS.from_documents(documents[:5], embedding=local_embeddings)
retriever = vectorstore.as_retriever()

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
    | llm
    | StrOutputParser()
)

question = "超标量处理是什么" 
response = chain.invoke(question)
print(response)