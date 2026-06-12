# DataDash — Real-time Crypto Market Dashboard

A professional cryptocurrency market dashboard built with vanilla JavaScript, Chart.js, and the CoinGecko API. Demonstrates real-time data integration, interactive data visualization, and responsive UI design.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Built with](https://img.shields.io/badge/Built%20with-Vanilla%20JS-yellow)
![API](https://img.shields.io/badge/API-CoinGecko-green)

## Live Demo

**[View Live Demo →](https://9d3a10e4fbf34d52b55590d0f6e97950.app.codebuddy.work)** *(deployed via CloudStudio)*

## Features

- **Real-time Market Data** — Live prices, 24h volume, market cap from CoinGecko API
- **Interactive Price Charts** — BTC, ETH, XRP, SOL with 24H/7D/30D/90D time ranges
- **Top 100 Coin Explorer** — Searchable, sortable table with live price updates
- **Top Gainers & Losers** — 24h performance highlights
- **Auto-refresh** — Data refreshes every 60 seconds
- **Fully Responsive** — Works on desktop, tablet, and mobile
- **Dark Theme UI** — Modern, professional design with smooth animations

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript (ES6+) |
| **Charts** | Chart.js 4.x |
| **Data Source** | CoinGecko REST API (free tier) |
| **Deployment** | Vercel / CloudStudio / any static host |
| **Design** | Custom CSS Grid + Flexbox, CSS animations |

## Project Structure

```
datadash-mvp/
├── index.html          # Main application (self-contained)
├── README.md           # This file
└── assets/             # (optional) static assets
```

## Quick Start

No build step required. Just open `index.html` in any browser, or serve with any static file server:

```bash
# Using Python
python -m http.server 3000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:3000
```

## API

This project uses the [CoinGecko Public API](https://www.coingecko.com/en/api) (free, no API key required).

Endpoints used:
- `/api/v3/global` — Global market data
- `/api/v3/coins/markets` — Top 100 coins by market cap
- `/api/v3/coins/{id}/market_chart` — Historical price data

**Rate Limit:** 10-30 calls/minute (public API). The dashboard is optimized to stay within these limits.

## Why This Project?

Built to demonstrate:

1. **Real-time API Integration** — Fetching, caching, and displaying live financial data
2. **Data Visualization** — Interactive Chart.js charts with multiple time series
3. **Production-quality UI** — Responsive design, loading states, error handling, dark theme
4. **Clean Architecture** — Well-organized vanilla JS without framework overhead

Ideal for showcasing data engineering + front-end skills to potential clients on Upwork.

## License

MIT — feel free to use this as a template for your own dashboard projects.
