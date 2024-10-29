// src/LimitOrderForm.js
import React, { useState } from 'react';
import axios from 'axios';

const LimitOrderForm = () => {
    const [orderId, setOrderId] = useState('');
    const [side, setSide] = useState('buy'); // Default to buy
    const [size, setSize] = useState('');
    const [ticker, setTicker] = useState('');
    const [price, setPrice] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const orderData = {
                id: orderId,
                side,
                size: parseInt(size),
                ticker,
                price: parseFloat(price),
            };

            const response = await axios.post('http://localhost:8000/create_limit_order', orderData);
            setMessage(`Order created successfully: ${response.data.message}`);
            // Reset form fields after submission
            setOrderId('');
            setSize('');
            setTicker('');
            setPrice('');
        } catch (error) {
            setMessage(`Error creating order: ${error.response?.data?.error || error.message}`);
        }
    };

    return (
        <div>
            <h2>Create Limit Order</h2>
            <form onSubmit={handleSubmit}>
                <select value={side} onChange={(e) => setSide(e.target.value)} required>
                    <option value="buy">Buy</option>
                    <option value="sell">Sell</option>
                </select>
                <input
                    type="number"
                    placeholder="Size"
                    value={size}
                    onChange={(e) => setSize(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Ticker"
                    value={ticker}
                    onChange={(e) => setTicker(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Price"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    required
                />
                <button type="submit">Create Order</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default LimitOrderForm;