from flask import Flask, request, jsonify
from agents.knowledge_agent import KnowledgeAgent

app = Flask(__name__)
knowledge_agent = KnowledgeAgent()

@app.route('/api/query', methods=['POST'])
def query_agent():
    data = request.json
    user_query = data.get('query')
    response = knowledge_agent.create_agent(user_query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)