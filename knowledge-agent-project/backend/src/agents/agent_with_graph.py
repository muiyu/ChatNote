from services.graph_rag import GraphRAGService

def process_markdown_with_graph(markdown_content, question):
    service = GraphRAGService(markdown_content=markdown_content, question=question)
    response = service.process_query()
    return response

def process_question_with_graph(question):
    service = GraphRAGService(markdown_content=None, question=question)
    response = service.process_query()
    return response