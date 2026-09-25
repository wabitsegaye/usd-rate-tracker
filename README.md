# USD Exchange Rate Tracker

Collects hourly USD exchange rate snapshots via GitHub Actions and analyzes
the trend with pandas.

Tracked currencies: EUR, GBP, ETB, JPY, CAD, AUD, CHF, CNY, INR, KES
API: [exchangerate-api.com Open Access](https://www.exchangerate-api.com/docs/free) — no key required.

## How it works

- .github/workflows/hourly_rates.yml runs fetch_rates.py every hour via
  GitHub Actions cron, and commits the result back to the repo.
- fetch_rates.py saves each run as data/rates_<timestamp>.json and also
  appends a row to data/rates_history.csv. It automatically stops
  collecting once 12 snapshots exist (a ~12-hour window at 1/hour).
- analyze_rates.py loads data/rates_history.csv with pandas, prints
  summary stats, and saves a line chart to data/rates_over_time.png.

## Setup (from zero)

1. Create a new repo on GitHub, no README needed since you'll push these files.
2. Push these files to the repo, keeping the .github/workflows/ folder path.
3. In your repo, go to **Settings → Actions → General → Workflow
   permissions, and select "Read and write permissions"** (the workflow
   needs this to commit data back).
4. Go to the Actions tab, click "Hourly Exchange Rate Collector," click
   Run workflow to trigger it manually right away.

## Running the analysis

After a few snapshots have been collected:

`bash
pip install -r requirements.txt
python analyze_rates.py
