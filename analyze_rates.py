#!/usr/bin/env python3
"""
Load the collected exchange-rate history and plot each currency over time.

Reads: data/rates_history.csv (written incrementally by fetch_rates.py)
Writes: data/rates_over_time.png
"""

import os

import matplotlib
matplotlib.use("Agg")  # headless-safe backend for CI
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(file)), "data")
HISTORY_CSV = os.path.join(DATA_DIR, "rates_history.csv")
OUTPUT_PNG = os.path.join(DATA_DIR, "rates_over_time.png")


def load_history() -> pd.DataFrame:
    if not os.path.isfile(HISTORY_CSV):
        raise FileNotFoundError(
            f"No history file found at {HISTORY_CSV}. Run fetch_rates.py first "
            "(or let the scheduled workflow collect a few snapshots)."
        )
    df = pd.read_csv(HISTORY_CSV, parse_dates=["timestamp_utc"])
    df = df.sort_values("timestamp_utc").set_index("timestamp_utc")
    return df


def plot_history(df: pd.DataFrame) -> None:
    currency_cols = [c for c in df.columns]

    fig, ax = plt.subplots(figsize=(11, 6))
    for col in currency_cols:
        ax.plot(df.index, df[col], marker="o", label=col)

    ax.set_title("USD Exchange Rates Over Time")
    ax.set_xlabel("Timestamp (UTC)")
    ax.set_ylabel("Rate (units per 1 USD)")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=150)
    print(f"Saved chart -> {OUTPUT_PNG}")


def print_summary(df: pd.DataFrame) -> None:
    print("\n=== Summary statistics ===")
    print(df.describe().T[["mean", "std", "min", "max"]])

    if len(df) >= 2:
        print("\n=== % change, first snapshot -> latest ===")
        pct_change = ((df.iloc[-1] - df.iloc[0]) / df.iloc[0] * 100).round(3)
        print(pct_change.to_string())


def main():
    df = load_history()
    print(f"Loaded {len(df)} snapshot(s) covering "
          f"{df.index.min()} to {df.index.max()}")
    print_summary(df)
    plot_history(df)


if name == "main":
    main()
