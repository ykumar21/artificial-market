import React, { useState, useEffect } from 'react';
import { useSocket } from './../../SocketContext'; // Import the hook

const OrderBook = () => {
    const [bids, setBids] = useState([]);
    const [asks, setAsks] = useState([]);

    // Connect to the WebSocket server
    const socket = useSocket();

    useEffect(() => {
        if (socket) {
            // Listen for bids
            socket.on('bids', (bidData) => {
                console.log("Recieved Bid Data")
                setBids( JSON.parse(bidData) );
                console.log(bidData)
            });
            // Listen for asks
            socket.on('asks', (askData) => {
                console.log("Recieved Ask Data")
                setAsks(askData);
            });

            // Cleanup the socket listener on unmount
            return () => {
                socket.off('bids'); // Remove the listener
            };
        }
    }, [socket]);

    return (
        <div class="order-book">
          <h2 class="heading">Order Book</h2>
          <table class="table">
            <thead>
              <tr>
                <th>Price(USD)</th>
                <th>Amount(SZ)</th>
                <th>Volume(SH)</th>
              </tr>
            </thead>
            {Object.entries(bids).map(([ticker, data]) => (
            <tbody>
                {data.prices.map((price, index) => (
                      <tr class={`red-bg`}>
                        <td class="red">{price}</td>
                        <td>{data.volumes[index]}</td>
                        <td>15.25458</td>
                      </tr>
                ))}
            </tbody>
            ))}
            <tbody class="ob-heading">
              <tr>
                <td>
                  <span>Last Price</span>
                  0.020367
                </td>
                <td>
                  <span>USD</span>
                  148.65
                </td>
                <td class="red">
                  <span>Change</span>
                  -0.51%
                </td>
              </tr>
            </tbody>
            <tbody>
              <tr class="green-bg">
                <td class="green">0.158373</td>
                <td>1.209515</td>
                <td>15.23248</td>
              </tr>
              <tr class="green-bg-5">
                <td class="green">0.020851</td>
                <td>1.206245</td>
                <td>15.25458</td>
              </tr>
              <tr class="green-bg-8">
                <td class="green">0.025375</td>
                <td>1.205715</td>
                <td>15.65648</td>
              </tr>
              <tr class="green-bg-10">
                <td class="green">0.020252</td>
                <td>1.205495</td>
                <td>15.24548</td>
              </tr>
              <tr class="green-bg-20">
                <td class="green">0.020373</td>
                <td>1.205415</td>
                <td>15.25648</td>
              </tr>
              <tr class="green-bg-40">
                <td class="green">0.020156</td>
                <td>1.207515</td>
                <td>15.28948</td>
              </tr>
              <tr class="green-bg-60">
                <td class="green">0.540375</td>
                <td>1.205915</td>
                <td>15.25748</td>
              </tr>
              <tr class="green-bg-80">
                <td class="green">0.020372</td>
                <td>1.205415</td>
                <td>15.25648</td>
              </tr>
            </tbody>
          </table>
        </div>
    )
};

export default OrderBook;