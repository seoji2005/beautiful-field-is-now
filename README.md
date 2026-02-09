# beautiful-field-is-now
stock-insight

# 📈 Stock Insight CLI (Financial Data Analyzer)
# 株式市場インサイトCLI (金融データ分析ツール)

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas)](https://pandas.pydata.org/)
[![Rich](https://img.shields.io/badge/CLI-Rich-red)](https://github.com/Textualize/rich)

## 📖 Introduction

**English**
Stock Insight CLI is a lightweight, terminal-based financial analysis tool for developers and quantitative analysts. It fetches real-time stock data using **Yahoo Finance API**, processes technical indicators (RSI, Bollinger Bands, Moving Averages) using **Pandas**, and visualizes the insights with a beautiful UI powered by **Rich**.

**日本語**
Stock Insight CLIは、開発者やクオンツアナリスト向けの軽量なターミナルベース金融分析ツールです。**Yahoo Finance API**を使用してリアルタイムの株価データを取得し、**Pandas**を用いてテクニカル指標（RSI、ボリンジャーバンド、移動平均線）を計算、**Rich**ライブラリを活用して美しく可視化します。

---

## ⚡ Features

* **Real-time Data Fetching**: Retrieves the latest stock prices and historical data.
* **Technical Analysis**: Automatically calculates key indicators:
    * **RSI (Relative Strength Index)**: Detects overbought/oversold conditions.
    * **Bollinger Bands**: Analyzes volatility and price levels.
    * **Moving Averages (MA5, MA20)**: Identifies short-term trends.
* **Rich UI**: Provides a clean, dashboard-style interface directly in the terminal.

---

## 🛠 Tech Stack

* **Language**: Python 3.10
* **Data Source**: `yfinance` (Yahoo Finance API)
* **Data Processing**: `pandas`, `numpy`
* **Visualization**: `rich` (CLI Dashboard)

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the analyzer (Default: GOOGL)
python main.py