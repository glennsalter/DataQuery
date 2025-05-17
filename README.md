# Data Query Task
## Basic setup
```bash
python -m venv .venv
source .venv/bin/activate # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

## Approach #1 - Web Scraping
This approach uses `selenium` to scrape the announcement page.

Command:
```bash
python webscraper.py
```
Output files found in `output` folder:
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

Runtime logs:
```
Number of titles: 5
Elapsed time: 6.29 seconds
```

## Approach #2 - API
Command:
```bash
python apirequest.py --refresh_rate 60
```

Explanation:
- This script will use `selenium` to open the binance website to get the `cookies`.
- Once we get the cookies it is used to make API requests

Benefits:
- This speeds up the process as we don't have to open the browser for every request

Runtime logs:
```
Running with refresh rate: 10 seconds
Starting process at 20250517_161315
Number of titles: 5
Parsed announcements to output/20250517_161315_announcements.csv
Elapsed time: 0.32 seconds
Starting process at 20250517_161325
Number of titles: 5
Parsed announcements to output/20250517_161325_announcements.csv
Elapsed time: 0.19 seconds
Starting process at 20250517_161335
Number of titles: 5
Parsed announcements to output/20250517_161335_announcements.csv
Elapsed time: 0.32 seconds
Starting process at 20250517_161346
Number of titles: 5
Parsed announcements to output/20250517_161346_announcements.csv
Elapsed time: 0.42 seconds

```