import React, { useEffect, useState } from 'react';
import { useSocket } from './../../SocketContext'; // Import the hook
import axios from 'axios';

const ExchangeComponent = () => {
    const socket = useSocket(); // Get the socket from context
    const [exchangeId, setExchangeId] = useState('');
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        if (socket) {
            // Update connection status
            setIsConnected(socket.connected);

            // Listen for connection and disconnection events
            socket.on('connect', () => {
                setIsConnected(true);
            });

            socket.on('disconnect', () => {
                setIsConnected(false);
            });

            // Clean up the event listeners when the component unmounts
            return () => {
                socket.off('connect');
                socket.off('disconnect');
            };
        }
    }, [socket]);

    const initializeExchange = async () => {
        try {

            const response = await axios.post('http://localhost:8000/init', {
                exchange_id: exchangeId,
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error initializing exchange:', error.response.data);
        }
    };

    const subscribeToExchange = async () => {
        try {
            const response = await axios.post('http://localhost:8000/subscribe', {
                exchange_id: exchangeId,
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error subscribing to exchange:', error.response.data);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        initializeExchange();
        subscribeToExchange();
    };

    return (
        <div>
            <h2>Exchange Subscription</h2>
            <div>
                <strong>Socket Status: </strong>
                <span style={{ color: isConnected ? 'green' : 'red' }}>
                    {isConnected ? 'Connected' : 'Disconnected'}
                </span>
            </div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={exchangeId}
                    onChange={(e) => setExchangeId(e.target.value)}
                    placeholder="Enter Exchange ID"
                    required
                />
                <button type="submit">Initialize and Subscribe</button>
            </form>
        </div>
    );
};

export default ExchangeComponent;