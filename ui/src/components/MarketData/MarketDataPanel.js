import React from 'react';
import MarketDataTab from './MarketDataTab';

const MarketDataPanel = () => {
    return (
        <div class="market-pairs">
          <div class="input-group">
            <div class="input-group-prepend">
              <span class="input-group-text" id="inputGroup-sizing-sm"><i class="icon ion-md-search"></i></span>
            </div>
            <input type="text" class="form-control" placeholder="Search" aria-describedby="inputGroup-sizing-sm" />
          </div>
          <ul class="nav nav-pills" role="tablist">

            <li class="nav-item">
              <a class="nav-link" data-toggle="pill" href="#STAR" role="tab" aria-selected="true"><i class="icon ion-md-star"></i></a>
            </li>

          </ul>
          <div class="tab-content">
            <MarketDataTab />
          </div>
        </div>
        )
};

export default MarketDataPanel;