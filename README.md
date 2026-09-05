# NSE Bullish Stock Analyzer

A comprehensive Python-based stock market analysis tool with React Native mobile app to identify bullish stocks in the NSE (National Stock Exchange) for the coming week.

## Project Features

✅ **Backend API (Python/Flask)**
- Real-time NSE stock data fetching
- Technical indicator analysis (RSI, MACD, Moving Averages)
- Bullish pattern detection
- Weekly stock predictions
- REST API endpoints

✅ **Mobile App (React Native)**
- Cross-platform (iOS & Android)
- Real-time stock updates
- Push notifications for bullish signals
- Interactive charts and analysis
- Portfolio tracking

✅ **Data Sources**
- NSE API integration
- Yahoo Finance API
- Alpha Vantage

## Project Structure

```
nse-bullish-stock-analyzer/
├── backend/                    # Python Flask API
│   ├── app.py
│   ├── requirements.txt
│   ├── config.py
│   ├── models/
│   │   ├── stock_analyzer.py
│   │   ├── technical_indicators.py
│   │   └── bullish_detector.py
│   ├── routes/
│   │   ├── stocks.py
│   │   ├── analysis.py
│   │   └── predictions.py
│   ├── utils/
│   │   ├── nse_fetcher.py
│   │   ├── data_processor.py
│   │   └── cache.py
│   └── tests/
│       └── test_analyzer.py
│
├── mobile-app/                 # React Native Mobile App
│   ├── App.js
│   ├── package.json
│   ├── screens/
│   │   ├── HomeScreen.js
│   │   ├── StockDetailsScreen.js
│   │   ├── AnalysisScreen.js
│   │   └── PortfolioScreen.js
│   ├── components/
│   │   ├── StockCard.js
│   │   ├── ChartComponent.js
│   │   ├── TechnicalIndicators.js
│   │   └── NotificationHandler.js
│   ├── services/
│   │   ├── api.js
│   │   ├── localStorage.js
│   │   └── notifications.js
│   └── assets/
│       └── images/
│
├── frontend/                   # Web Dashboard (Optional)
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── components/
│
├── docs/                       # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── SETUP_GUIDE.md
│   └── ARCHITECTURE.md
│
├── .github/
│   └── workflows/
│       ├── python-tests.yml
│       └── mobile-build.yml
│
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── CONTRIBUTING.md
```

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Mobile App Setup
```bash
cd mobile-app
npm install
npm start
```

## API Endpoints

- `GET /api/stocks` - Get all bullish stocks
- `GET /api/stocks/{symbol}` - Get stock details
- `GET /api/analysis/{symbol}` - Get technical analysis
- `GET /api/predictions` - Get weekly predictions
- `POST /api/portfolio` - Add stock to portfolio

## Technical Stack

**Backend:**
- Python 3.9+
- Flask/FastAPI
- Pandas & NumPy
- TA-Lib (Technical Analysis)
- SQLite/PostgreSQL

**Mobile App:**
- React Native
- Redux (State Management)
- Axios (API Client)
- react-native-chart-kit (Charts)
- Firebase (Push Notifications)

**Data Processing:**
- Pandas
- TA-Lib
- SciPy

## Installation

### Prerequisites
- Python 3.9+
- Node.js 14+
- npm or yarn
- Git

### Steps
1. Clone the repository
2. Follow individual setup guides in backend/ and mobile-app/
3. Configure API keys in .env file
4. Run the application

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for details.

## License

MIT License - See LICENSE file

## Support

For issues and questions, please open a GitHub issue.

## Disclaimer

⚠️ **Important**: This tool is for educational and research purposes only. Stock market predictions are not guaranteed. Always do your own research and consult with a financial advisor before making investment decisions.
