# Data Query Task
## Basic setup
```bash
python -m venv .venv
source .venv/bin/activate # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

## Approach #1 - Web Scraping
Command:
```bash
python webscraper.py
```
Output results in `output` folder:
- `{timestamp}_announcements.csv` - CSV file containing the announcements data.

Should look like:
```
title
Binance Will Update the Collateral Ratio of Multiple Assets Under Portfolio Margin (2025-05-23)
SUI Ecosystem Trading Competition: Trade SUI Ecosystem Tokens on Binance Alpha and Share Approximately $1.7M Worth of Rewards
Binance Futures Will Launch USDⓈ-Margined CVCUSDT Perpetual Contract
Binance Earn: Enjoy 10% Bonus Tiered APR with USDC Flexible Products!
"Update on Zero Maker Fee Promotion for ARS, BRL & ZAR Spot Trading Pairs"
```

## Approach #2 - API
