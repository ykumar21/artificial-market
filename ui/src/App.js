import React from 'react';
import './css/App.css'; // Ensure you create this CSS file for styles
import Header from './components/common/Header';
import MarketDataPanel from './components/MarketData/MarketDataPanel';
import { SocketProvider } from './SocketContext';
import OrderForm from './components/Order/OrderForm'
import OrderBook from './components/Order/OrderBook'
import ExchangeComponent from './components/Exchange/ExchangeManager.js';

const App = () => {
  return (
  <SocketProvider>
  <ExchangeComponent />
    <div>
    <Header />
  <div class="container-fluid p-0">
    <div class="row no-gutters">
      <div class="col-md-3">
        <MarketDataPanel />
      </div>
      <div class="col-md-6">
        <div class="main-chart">
          <div class="tradingview-widget-container">
            <div id="tradingview_e8053"></div>
            <script src="js/tv.js"></script>

          </div>
        </div>
        <OrderForm />
      </div>
      <div class="col-md-3">
        <OrderBook />
        <div class="market-history">
          <ul class="nav nav-pills" role="tablist">
            <li class="nav-item">
              <a class="nav-link" data-toggle="pill" href="#recent-trades" role="tab" aria-selected="true">Recent
                Trades</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" data-toggle="pill" href="#market-depth" role="tab" aria-selected="false">Market
                Depth</a>
            </li>
          </ul>
          <div class="tab-content">
            <div class="tab-pane fade" id="recent-trades" role="tabpanel">
              <table class="table">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>Price(BTC)</th>
                    <th>Amount(ETH)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>13:03:53</td>
                    <td class="red">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="green">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="green">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="red">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="green">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="green">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="green">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="red">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="red">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="green">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="green">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="red">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="green">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                  <tr>
                    <td>13:03:53</td>
                    <td class="red">0.020191</td>
                    <td>0.2155045</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="tab-pane fade show active" id="market-depth" role="tabpanel">
              <div class="depth-chart-container">
                <div class="depth-chart-inner">
                  <div id="lightDepthChart"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script src="js/jquery-3.4.1.min.js"></script>
  <script src="js/popper.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/amcharts-core.min.js"></script>
  <script src="js/amcharts.min.js"></script>
  <script src="js/jquery.mCustomScrollbar.js"></script>
  <script src="js/custom.js"></script>
</div>
 </SocketProvider>
  );
};

export default App;