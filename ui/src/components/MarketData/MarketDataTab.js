import React, {useState, useEffect} from 'react';
import { useSocket } from './../../SocketContext'; // Import the hook

const MarketDataTab = () => {
    const socket = useSocket(); // Get the socket from context
    const [lastPrices, setLastPrices] = useState({

    });

    useEffect(() => {
        if (socket) {
            // Listen for the 'last_price' event
            socket.on('market_price_update', (data) => {
                console.log('Received last price data:', data);

                try {
                    const parsedData = typeof data === 'string' ? JSON.parse(data) : data; // Parse if it's a string
                    setLastPrices(parsedData); // Update state with the parsed JSON object
                } catch (error) {
                    console.error('Error parsing last price data:', error);
                }
            });

            // Cleanup the socket listener on unmount
            return () => {
                socket.off('market_price_update'); // Remove the listener
            };
        }
    }, [socket]);

    return (
        <div class="tab-pane fade show active" id="PAX" role="tabpanel">
              <table class="table">
                <thead>
                  <tr>
                    <th>Symbol</th>
                    <th>Last</th>
                    <th>Offer</th>
                    <th>Ask</th>
                    <th>Change</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(lastPrices).map(([ticker, { last_price, best_bid, best_ask, change }]) => (
                        <tr key={ticker}>
                            <td><i className="icon ion-md-star"></i>{ticker}</td>
                            <td>{last_price.toFixed(2)}</td>
                            <td>{best_bid.toFixed(2)}</td>
                            <td>{best_ask.toFixed(2)}</td>
                            <td className={change < 0 ? 'red' : 'green'}>{change.toFixed(2)}%</td>
                        </tr>
                    ))}
                </tbody>
              </table>
            </div>
    );
};

export default MarketDataTab;