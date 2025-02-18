import React, { useState } from 'react';
import axios from 'axios';

const OrderForm = () => {
    const [ticker, setTicker] = useState('');
    const [positionSize, setPositionSize] = useState('');
    const [limitPrice, setLimitPrice] = useState('');

    const handleBuy = async () => {
        try {
            let size = positionSize;
            let price = limitPrice;
            const orderData = {
                side: 'buy',
                ticker,
                size,
                price,
            };
            const response = await axios.post('http://localhost:8000/orders', orderData);
            console.log('Order response:', response.data);
            // Handle success (e.g., show a notification)
        } catch (error) {
            console.error('Error placing buy order:', error);
            // Handle error (e.g., show an error message)
        }
    };

    const handleSell = async () => {
        try {
            let size = positionSize;
            let price = limitPrice;
            const orderData = {
                side: 'sell',
                ticker,
                size,
                price,
            };
            console.log(orderData);
            const response = await axios.post('http://localhost:8000/orders', orderData);
            console.log('Order response:', response.data);
            // Handle success (e.g., show a notification)
        } catch (error) {
            console.error('Error placing sell order:', error);
            // Handle error (e.g., show an error message)
        }
    };

    return (
        <div className="market-trade">
            <ul className="nav nav-pills" role="tablist">
                <li className="nav-item">
                    <a className="nav-link active" data-toggle="pill" href="#pills-trade-limit" role="tab" aria-selected="true">Limit</a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" data-toggle="pill" href="#pills-market" role="tab" aria-selected="false">Market</a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" data-toggle="pill" href="#pills-stop-limit" role="tab" aria-selected="false">Stop Limit</a>
                </li>
                <li className="nav-item">
                    <a className="nav-link" data-toggle="pill" href="#pills-stop-market" role="tab" aria-selected="false">Stop Market</a>
                </li>
            </ul>
            <div className="tab-content">
                <div className="tab-pane fade show active" id="pills-trade-limit" role="tabpanel">
                    <div className="d-flex justify-content-between">
                        <div className="market-trade-buy">
                            <div className="input-group">
                                <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Ticker"
                                    value={ticker}
                                    onChange={(e) => setTicker(e.target.value)}
                                />
                                <div className="input-group-append">
                                    <span className="input-group-text">Ticker</span>
                                </div>
                            </div>
                            <div className="input-group">
                                <input
                                    type="number"
                                    className="form-control"
                                    placeholder="Position Size"
                                    value={positionSize}
                                    onChange={(e) => setPositionSize(e.target.value)}
                                />
                                <div className="input-group-append">
                                    <span className="input-group-text">Share</span>
                                </div>
                            </div>
                            <div className="input-group">
                                <input
                                    type="number"
                                    className="form-control"
                                    placeholder="Price"
                                    value={limitPrice}
                                    onChange={(e) => setLimitPrice(e.target.value)}
                                />
                                <div className="input-group-append">
                                    <span className="input-group-text">Limit Price</span>
                                </div>
                            </div>
                            <ul className="market-trade-list">
                                <li><a href="#!">25%</a></li>
                                <li><a href="#!">50%</a></li>
                                <li><a href="#!">75%</a></li>
                                <li><a href="#!">100%</a></li>
                            </ul>
                            <p>Available: <span>0 BTC = 0 USD</span></p>
                            <p>Volume: <span>0 BTC = 0 USD</span></p>
                            <button className="btn buy" onClick={handleBuy}>Buy</button>
                        </div>
                        <div className="market-trade-sell">
                            <div className="input-group">
                                <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Ticker"
                                    value={ticker}
                                    onChange={(e) => setTicker(e.target.value)}
                                />
                                <div className="input-group-append">
                                    <span className="input-group-text">Ticker</span>
                                </div>
                            </div>
                            <div className="input-group">
                                <input
                                    type="number"
                                    className="form-control"
                                    placeholder="Position Size"
                                    value={positionSize}
                                    onChange={(e) => setPositionSize(e.target.value)}
                                />
                                <div className="input-group-append">
                                    <span className="input-group-text">Share</span>
                                </div>
                            </div>
                            <div className="input-group">
                                <input
                                    type="number"
                                    className="form-control"
                                    placeholder="Price"
                                    value={limitPrice}
                                    onChange={(e) => setLimitPrice(e.target.value)}
                                />
                                <div className="input-group-append">
                                    <span className="input-group-text">Limit Price</span>
                                </div>
                            </div>
                            <ul className="market-trade-list">
                                <li><a href="#!">25%</a></li>
                                <li><a href="#!">50%</a></li>
                                <li><a href="#!">75%</a></li>
                                <li><a href="#!">100%</a></li>
                            </ul>
                            <p>Available: <span>0 BTC = 0 USD</span></p>
                            <p>Volume: <span>0 BTC = 0 USD</span></p>
                            <button className="btn sell" onClick={handleSell}>Sell</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OrderForm;