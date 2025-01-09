from services.deepseek_v2_langchain import LangChainService

def process_markdown_with_llm(markdown_content, question):
    service = LangChainService(markdown_content, question)
    response = service.process_query()
    return response

def process_question_only(question):
    """
    处理仅回答问题（无需上传文件）。
    """
    try:
        # 初始化 LangChainService，不传入 markdown_content
        service = LangChainService(question=question)
        # 处理查询)
        response = service.process_query()
        print(f"Response: {response}")
        return response
    except Exception as e:
        print(f"Error in process_question_only: {str(e)}")
        return f"Error: {str(e)}"