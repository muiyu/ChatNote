export const fetchAgentResponse = async (query) => {
    try {
        const response = await fetch('/api/agent/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching agent response:', error);
        throw error;
    }
};