// src/ExchangeManager.js
import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import axios from 'axios';

const ExchangeManager = () => {
    const [exchangeId, setExchangeId] = useState('');
    const [message, setMessage] = useState('');
    const [sessionManagers, setSessionManagers] = useState([]);

    const handleInitExchange = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/init', { exchange_id: exchangeId });
            console.log(response)
            setMessage(response.data.message);
            setSessionManagers([...sessionManagers, exchangeId]);
        } catch (error) {
            setMessage(error.response.data.error);
        }
    };

    const handleSubscribe = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/subscribe', { exchange_id: exchangeId });
            setMessage('Subscribed successfully to exchange');
        } catch (error) {
            setMessage(error.response.data.error);
        }
    };

    return (
        <div>
            <h1>Exchange Manager</h1>
            <form onSubmit={handleInitExchange}>
                <input
                    type="text"
                    placeholder="Enter Exchange ID"
                    value={exchangeId}
                    onChange={(e) => setExchangeId(e.target.value)}
                    required
                />
                <button type="submit">Initialize Exchange</button>
            </form>

            <form onSubmit={handleSubscribe}>
                <input
                    type="text"
                    placeholder="Enter Exchange ID to Subscribe"
                    value={exchangeId}
                    onChange={(e) => setExchangeId(e.target.value)}
                    required
                />
                <button type="submit">Subscribe</button>
            </form>

            {message && <p>{message}</p>}

            <h2>Active Exchanges:</h2>
            <ul>
                {sessionManagers.map((id, index) => (
                    <li key={index}>{id}</li>
                ))}
            </ul>
        </div>
    );
};

export default ExchangeManager;