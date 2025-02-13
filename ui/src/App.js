import React, { useEffect, useState } from 'react';
import ExchangeManager from './components/ExchangeManager';
import LimitOrderForm from "./components/LimitOrderForm";
import { io } from "socket.io-client";
import { parseBboUpdate } from "./utils/bboUtils";
import ArrayVisualizer from "./ArrayVisualizer";
import LineChart from "./Linechart";
import './App.css';
import AgentMenu from "./components/AgentsMenu"; // Import the CSS file

const socket = io('http://localhost:8000'); // Adjust the URL as needed

function App() {
    const [bboData, setBboData] = useState({ bestBid: '', bestAsk: '' });
    const [lastPrice, setLastPrice] = useState([]);
    const [bids, setBids] = useState([]);
    const [asks, setAsks] = useState([]);
    const [isDarkMode, setIsDarkMode] = useState(false);

    const toggleDarkMode = () => {
        setIsDarkMode(!isDarkMode);
        if (!isDarkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    };

    const appendLastPrice = (latestPrice) => {
        setLastPrice(prevItems => [...prevItems, latestPrice]);
    };

    useEffect(() => {
        socket.on('bbo_update', (data) => {
            const parsedUpdate = parseBboUpdate(data);
            if (parsedUpdate) {
                setBboData(parsedUpdate);
            }
        });

        socket.on('last_price', (data) => {
            appendLastPrice(data);
        });

        socket.on('bids', (data) => {
            setBids(data);
        });

        socket.on('asks', (data) => {
            setAsks(data);
        });

        return () => {
            socket.off('connect');
            socket.off('bbo_update');
        };
    }, []);

    return (
        <div className="container">
            <h1>Trading Dashboard</h1>
            <button onClick={toggleDarkMode} className="button">
                Toggle Dark Mode
            </button>

            <section className="section">
                <ExchangeManager />
                <LimitOrderForm />
            </section>

            <section className="section flex-container">
                <div className="order-book">
                    <ArrayVisualizer array1={bids} array2={asks} />
                </div>

                <div className="chart-container">
                    <h2>Last Traded Price Visualization</h2>
                    <LineChart prices={lastPrice} />
                </div>
            </section>

            <AgentMenu />

            <section className="section">
                <h2>BBO Updates</h2>
                <div className="bbo-updates">
                    {bboData.bestBid && bboData.bestAsk ? (
                        <div>
                            <p className="bbo-title">Current BBO:</p>
                            <p><strong>Best Bid:</strong> {bboData.bestBid}</p>
                            <p><strong>Best Ask:</strong> {bboData.bestAsk}</p>
                        </div>
                    ) : (
                        <p>No BBO updates received yet.</p>
                    )}
                </div>
            </section>
        </div>
    );
}

export default App;