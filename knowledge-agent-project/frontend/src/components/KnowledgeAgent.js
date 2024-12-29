import React, { useState } from 'react';
import { fetchAgentResponse } from '../services/api';
import './KnowledgeAgent.css';

const KnowledgeAgent = () => {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResponse('');

        try {
            const result = await fetchAgentResponse(query);
            setResponse(result);
        } catch (error) {
            setResponse('Error fetching response');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="knowledge-agent">
            <h1>知识库代理</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={query}
                    onChange={handleQueryChange}
                    placeholder="输入你的问题"
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? '加载中...' : '提交'}
                </button>
            </form>
            {response && (
                <div className="response">
                    <h2>响应:</h2>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
};

export default KnowledgeAgent;