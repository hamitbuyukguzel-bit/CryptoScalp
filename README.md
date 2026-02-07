# CryptoScalp: Algorithmic Scalping & Momentum Scanner

CryptoScalp is a quantitative trading tool designed for high-frequency market analysis. It automates the detection of **Mean Reversion** opportunities by leveraging statistical indicators like Bollinger Bands and the Relative Strength Index (RSI).

## 🚀 Overview
In volatile markets like Bitcoin (BTC), manual scalping is inefficient and prone to emotional bias. This tool processes real-time price action to identify statistical anomalies—specifically when an asset is mathematically "Oversold" or "Overbought" relative to its recent volatility.

## 🧠 The Strategy (Mean Reversion)
The algorithm relies on the statistical probability that price will revert to its mean after an extreme deviation.

* **Buy Signal (Long):** * Price breaks below the **Lower Bollinger Band** (2 Standard Deviations).
    * **RSI (14)** drops below 30 (Indicating momentum exhaustion).
* **Sell Signal (Short):**
    * Price breaks above the **Upper Bollinger Band**.
    * **RSI (14)** exceeds 70 (Indicating overextension).

## 🛠 Tech Stack
* **Python:** Core algorithmic logic.
* **Pandas-TA:** Technical Analysis library for indicator calculation.
* **Streamlit:** Real-time dashboard and UI.
* **Plotly:** Interactive financial charting.
* **Yfinance:** Live market data ingestion.

## 📦 Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/crypto-scalp.git](https://github.com/YOUR_USERNAME/crypto-scalp.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    streamlit run app.py
    ```

## ⚠️ Disclaimer
This software is for **educational and research purposes only**. It does not constitute financial advice. Cryptocurrency trading involves significant risk. The author is not responsible for any financial losses.

---
*Author: [Your Name]*
