import React from 'react';

const Header = () => {
    return (
        <div>
            <header>
                <nav className="navbar navbar-expand-lg">
                    <a className="navbar-brand" href="/exchange-light">
                        <img src="images/logo-dark.svg" alt="logo" />
                    </a>
                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#headerMenu" aria-controls="headerMenu" aria-expanded="false" aria-label="Toggle navigation">
                        <i className="icon ion-md-menu"></i>
                    </button>

                    <div className="collapse navbar-collapse" id="headerMenu">
                        <ul className="navbar-nav mr-auto">
                            <li className="nav-item dropdown">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Landing Page
                                </a>
                                <div className="dropdown-menu">
                                    <a className="dropdown-item" href="/landing-page-light">Landing One</a>
                                    <a className="dropdown-item" href="/landing-page-light-two">Landing Two</a>
                                </div>
                            </li>
                            <li className="nav-item dropdown">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Exchange
                                </a>
                                <div className="dropdown-menu">
                                    <a className="dropdown-item" href="/exchange-light">Exchange</a>
                                    <a className="dropdown-item" href="/exchange-light-live-price">Exchange Live Price</a>
                                    <a className="dropdown-item" href="/exchange-light-ticker">Exchange Ticker</a>
                                    <a className="dropdown-item" href="/exchange-light-fluid">Exchange Fluid</a>
                                </div>
                            </li>
                            <li className="nav-item dropdown">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Markets
                                </a>
                                <div className="dropdown-menu">
                                    <a className="dropdown-item" href="/markets-light">Markets</a>
                                    <a className="dropdown-item" href="/market-capital-light">Markets Line</a>
                                    <a className="dropdown-item" href="/market-capital-bar-light">Markets Bar</a>
                                    <a className="dropdown-item" href="/market-overview-light">Market Overview</a>
                                    <a className="dropdown-item" href="/market-screener-light">Market Screener</a>
                                    <a className="dropdown-item" href="/market-crypto-light">Market Crypto</a>
                                </div>
                            </li>
                            <li className="nav-item dropdown">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Dashboard
                                </a>
                                <div className="dropdown-menu">
                                    <a className="dropdown-item" href="/settings-profile-light">Profile</a>
                                    <a className="dropdown-item" href="/settings-wallet-light">Wallet</a>
                                    <a className="dropdown-item" href="/settings-light">Settings</a>
                                </div>
                            </li>
                            <li className="nav-item dropdown">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Others
                                </a>
                                <div className="dropdown-menu">
                                    <a className="dropdown-item" href="/technical-analysis-light">Technical Analysis</a>
                                    <a className="dropdown-item" href="/cross-rates-light">Cross Rates</a>
                                    <a className="dropdown-item" href="/symbol-info-light">Symbol Info</a>
                                    <a className="dropdown-item" href="/heat-map-light">Heat Map</a>
                                    <a className="dropdown-item" href="/signin-light">Sign in</a>
                                    <a className="dropdown-item" href="/signup-light">Sign up</a>
                                    <a className="dropdown-item" href="/404-light">404</a>
                                </div>
                            </li>
                        </ul>
                        <ul className="navbar-nav ml-auto">
                            <li className="nav-item header-custom-icon">
                                <a className="nav-link" href="#" id="clickFullscreen">
                                    <i className="icon ion-md-expand"></i>
                                </a>
                            </li>
                            <li className="nav-item dropdown header-custom-icon">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <i className="icon ion-md-notifications"></i>
                                    <span className="circle-pulse"></span>
                                </a>
                                <div className="dropdown-menu">
                                    <div className="dropdown-header d-flex align-items-center justify-content-between">
                                        <p className="mb-0 font-weight-medium">6 New Notifications</p>
                                        <a href="#!" className="text-muted">Clear all</a>
                                    </div>
                                    <div className="dropdown-body">
                                        <a href="#!" className="dropdown-item">
                                            <div className="icon">
                                                <i className="icon ion-md-lock"></i>
                                            </div>
                                            <div className="content">
                                                <p>Account password change</p>
                                                <p className="sub-text text-muted">5 sec ago</p>
                                            </div>
                                        </a>
                                        <a href="#!" className="dropdown-item">
                                            <div className="icon">
                                                <i className="icon ion-md-alert"></i>
                                            </div>
                                            <div className="content">
                                                <p>Solve the security issue</p>
                                                <p className="sub-text text-muted">10 min ago</p>
                                            </div>
                                        </a>
                                        <a href="#!" className="dropdown-item">
                                            <div className="icon">
                                                <i className="icon ion-logo-android"></i>
                                            </div>
                                            <div className="content">
                                                <p>Download android app</p>
                                                <p className="sub-text text-muted">1 hrs ago</p>
                                            </div>
                                        </a>
                                        <a href="#!" className="dropdown-item">
                                            <div className="icon">
                                                <i className="icon ion-logo-bitcoin"></i>
                                            </div>
                                            <div className="content">
                                                <p>Bitcoin price is high now</p>
                                                <p className="sub-text text-muted">2 hrs ago</p>
                                            </div>
                                        </a>
                                        <a href="#!" className="dropdown-item">
                                            <div className="icon">
                                                <i className="icon ion-logo-usd"></i>
                                            </div>
                                            <div className="content">
                                                <p>Payment completed</p>
                                                <p className="sub-text text-muted">4 hrs ago</p>
                                            </div>
                                        </a>
                                    </div>
                                    <div className="dropdown-footer d-flex align-items-center justify-content-center">
                                        <a href="#!">View all</a>
                                    </div>
                                </div>
                            </li>
                            <li className="nav-item dropdown header-img-icon">
                                <a className="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    <img src="images/avatar.svg" alt="avatar" />
                                </a>
                                <div className="dropdown-menu">
                                    <div className="dropdown-header d-flex flex-column align-items-center">
                                        <div className="figure mb-3">
                                            <img src="images/avatar.svg" alt="" />
                                        </div>
                                        <div className="info text-center">
                                            <p className="name font-weight-bold mb-0">Tony Stark</p>
                                            <p className="email text-muted mb-3">tonystark@gmail.com</p>
                                        </div>
                                    </div>
                                    <div className="dropdown-body">
                                        <ul className="profile-nav">
                                            <li className="nav-item">
                                                <a className="nav-link" href="/settings-profile-light">
                                                    <i className="icon ion-md-person"></i>
                                                    <span>Profile</span>
                                                </a>
                                            </li>
                                            <li className="nav-item">
                                                <a className="nav-link" href="/settings-wallet-light">
                                                    <i className="icon ion-md-wallet"></i>
                                                    <span>My Wallet</span>
                                                </a>
                                            </li>
                                            <li className="nav-item">
                                                <a className="nav-link" href="/settings-light">
                                                    <i className="icon ion-md-settings"></i>
                                                    <span>Settings</span>
                                                </a>
                                            </li>
                                            <li className="nav-item" id="changeThemeLight">
                                                <a href="#!" className="nav-link">
                                                    <i className="icon ion-md-sunny"></i>
                                                    <span>Theme</span>
                                                </a>
                                            </li>
                                            <li className="nav-item">
                                                <a className="nav-link red" href="/exchange-light">
                                                    <i className="icon ion-md-power"></i>
                                                    <span>Log Out</span>
                                                </a>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </nav>
            </header>
        </div>
    );
};

export default Header;