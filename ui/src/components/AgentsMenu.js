import React, { useEffect, useState } from 'react';

const AgentMenu = () => {
    const [agents, setAgents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAgents = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/agents');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setAgents(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAgents();
    }, []);

    const handleAddAgent = async (agentName) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/agents', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ agent_name: agentName }),
            });
            if (!response.ok) {
                throw new Error('Failed to create agent');
            }
            const result = await response.json();
            console.log(result.message); // You can handle the success message as needed
        } catch (err) {
            setError(err.message);
        }
    };

    if (loading) return <p>Loading agents...</p>;
    if (error) return <p>Error fetching agents: {error}</p>;

    return (
        <div className="agent-menu">
            <h3>Select Agents to Add</h3>
            <div className="agent-list">
                {agents.map((agent, index) => (
                    <div key={index} className="agent-card">
                        <div className="agent-details">
                            <h4>{agent}</h4>
                            <p>{agent}</p> {/* Assuming the config is the same as the name for now */}
                        </div>
                        <button onClick={() => handleAddAgent(agent)} className="add-button">+</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AgentMenu;