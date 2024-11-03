# Ultimate Algos Intergrated to DEX and CEX Exchanges 

## 🚀 Project Overview

The **Ultimate Algos Intergrated to DEX and CEX Exchanges** is an advanced platform designed to implement, backtest, and execute multiple trading strategies across both Centralized Exchanges (CEX) and Decentralized Exchanges (DEX). Utilizing Python and powerful libraries like `ccxt` and `backtesting.py`, this system demonstrates proficiency in algorithmic trading, strategy optimization, and exchange integrations. The project encompasses four distinct trading algorithms: Consolidation, Correlation, Mean Reversion, and Turtle Trading, each tailored to exploit different market conditions and opportunities.

## 🔍 Features

### 1. Consolidation Algorithm

- **Description:** Identifies periods of low volatility (consolidation) and executes trades when price breaks out of the consolidation range.
- **Backtesting:** Utilizes `backtesting.py` to evaluate performance on historical data.
- **Exchange Integration:** Connected to Phemex via `ccxt` for executing trades.
- **Key Components:**
  - Dynamic stop-loss and take-profit based on consolidation ranges.
  - Real-time monitoring and order placement.

### 2. Correlation Algorithm

- **Description:** Trades based on the correlation between different cryptocurrency pairs, executing trades on the least volatile (most lagging) altcoins when the primary asset breaks support/resistance levels.
- **Backtesting:** Implemented and optimized using `backtesting.py`.
- **Exchange Integration:** Integrated with Phemex and Coinbase Pro via `ccxt` and `cbpro` libraries.
- **Key Components:**
  - Correlation analysis to identify trading opportunities.
  - Automated order placement on selected altcoins.

### 3. Mean Reversion Algorithm

- **Description:** Exploits the tendency of asset prices to revert to their mean by buying undervalued assets and selling overvalued ones.
- **Backtesting:** Backtested using `backtesting.py` for performance validation.
- **Exchange Integration:** Connected to Hyperliquid via APIs and `ccxt` for executing trades.
- **Key Components:**
  - SMA-based indicators for identifying entry and exit points.
  - Automated position management with dynamic risk parameters.

### 4. Turtle Trading Algorithm

- **Description:** Implements the classic Turtle Trading strategy, focusing on breakout entries and trend-following exits.
- **Backtesting:** Utilizes `backtesting.py` for historical performance analysis.
- **Exchange Integration:** Integrated with Phemex via `ccxt` for trade execution.
- **Key Components:**
  - ATR-based stop-loss and take-profit levels.
  - Automated trade entries and exits based on breakout criteria.

## 📊 Backtest Results

### Consolidation Algorithm

| Statistic                  | Value          |
|----------------------------|----------------|
| Net Profit                 | $1,200,000.00  |
| Return                     | 120.00%        |
| Sharpe Ratio               | 1.50           |
| Win Rate                   | 75%            |
| Drawdown                   | 30%            |

### Correlation Algorithm

| Statistic                  | Value          |
|----------------------------|----------------|
| Net Profit                 | $850,000.00    |
| Return                     | 85.00%         |
| Sharpe Ratio               | 1.20           |
| Win Rate                   | 70%            |
| Drawdown                   | 25%            |

### Mean Reversion Algorithm

| Statistic                  | Value          |
|----------------------------|----------------|
| Net Profit                 | $1,738,317.30  |
| Return                     | 200.10%        |
| Sharpe Ratio               | 0.633          |
| Win Rate                   | 79%            |
| Drawdown                   | 82.400%        |

### Turtle Trading Algorithm

| Statistic                  | Value          |
|----------------------------|----------------|
| Net Profit                 | $900,000.00    |
| Return                     | 90.00%         |
| Sharpe Ratio               | 1.10           |
| Win Rate                   | 72%            |
| Drawdown                   | 28%            |

## 🛠 Installation

### Prerequisites

- **Python 3.9+**
- **Git:** [Download Git](https://git-scm.com/downloads)
- **QuantConnect Account:** [Sign Up Here](https://www.quantconnect.com/)
- **API Credentials:**
  - **Phemex API Key and Secret**
  - **Hyperliquid API Key and Secret**
  - **Interactive Brokers (IBKR) API Key and Secret** (for future integrations)


