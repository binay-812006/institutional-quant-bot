<div align="center">

# Institutional Quant Bot

### Quantitative Trading Research Framework

Feature Engineering • Meta Labeling • Walk-Forward Validation • Portfolio Allocation • Mean Reversion Strategies

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Status](https://img.shields.io/badge/Status-Research-orange)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## Overview

Institutional Quant Bot is a modular quantitative trading research framework designed for developing, testing, and evaluating systematic trading strategies.

The project focuses on:

* Feature Engineering
* Multi-Timeframe Analysis
* Meta Labeling
* Ensemble Machine Learning
* Walk-Forward Validation
* Risk Management
* Portfolio Allocation
* Mean Reversion Strategies

The architecture is designed so that each component can be independently improved and evaluated.

---

## Current Architecture

```text
Market Data
      │
      ▼
Feature Engineering
      │
      ▼
Meta Labeling
      │
      ▼
Machine Learning Models
(RF + LR + GB)
      │
      ▼
Confidence Engine
      │
      ▼
Walk-Forward Validation
      │
      ▼
Strategy Engines
 ├── Bullish Mean Reversion
 └── Bearish Mean Reversion
      │
      ▼
Portfolio Allocation
      │
      ▼
Backtesting & Evaluation
```

---

## Features

### Feature Engineering

* Returns
* Log Returns
* Volatility
* Momentum
* ATR
* RSI
* Z-Score
* Relative Volume
* Trend Persistence
* Trend Exhaustion
* Volatility Expansion
* Momentum Exhaustion

### Meta Labeling

Triple Barrier Method:

* ATR-Based Take Profit
* ATR-Based Stop Loss
* Time Barrier

### Machine Learning

Ensemble Models:

* Random Forest
* Logistic Regression
* Gradient Boosting

### Validation

* Walk-Forward Testing
* Out-of-Sample Evaluation
* Rolling Capital Tracking

### Risk Management

* ATR-Based Position Sizing
* Drawdown Control
* Dynamic Risk Adjustment

---

## Strategy Engines

### Bullish Mean Reversion Engine

Entry Conditions:

* RSI < 35
* Z-Score < -1
* EMA20 > EMA50
* Positive Trend Strength
* Low Volatility Regime

### Bearish Mean Reversion Engine

Entry Conditions:

* RSI > 70
* Z-Score > 1
* EMA20 < EMA50
* Negative Trend Strength
* High Volatility Regime

---

## Current Research Results

### Bullish Mean Reversion

Initial Capital:

100,000

Final Capital:

101,168.70

Average Trade Profit:

194.78

### Portfolio Allocation Research

Tested allocations:

* 70 / 30
* 80 / 20
* 90 / 10
* 100 / 0

Current research suggests that the Bullish Mean Reversion Engine is the strongest-performing strategy.

---

## Project Structure

```text
institutional_quant_bot/

├── main.py
├── feature_engineering.py
├── meta_labeling.py
├── confidence_engine.py
├── ensemble_engine.py
├── risk_engine.py
├── backtester.py
├── walkforward_engine.py
├── bullish_mean_reversion_engine.py
├── bearish_mean_reversion_engine.py
├── portfolio_allocator.py
├── portfolio_manager.py
└── requirements.txt
```

---

## Installation

```bash
git clone https://github.com/binay-812006/institutional-quant-bot.git

cd institutional_quant_bot

pip install -r requirements.txt

python main.py
```

---

## Future Development

* Bearish Mean Reversion V2
* Dynamic Portfolio Allocation
* Regime Detection Improvements
* Advanced Risk Management
* Live Trading Integration
* Performance Analytics Dashboard

---

## Author

Binay Duary

B.Tech Computer Science and Engineering

Quantitative Trading Research Project

---

## Disclaimer

This project is intended for educational and research purposes only.

It does not constitute financial advice.
