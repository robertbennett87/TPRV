#!/usr/bin/env python3
"""Render HISTORY.md from history/scores.csv.

The CSV is long-format: timestamp_utc,commodity,score,label,driver — one row
per commodity per run. Output is a wide table (runs as rows, newest first)
plus a recent-trend line per commodity.
"""
import csv
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "history" / "scores.csv"
OUT_PATH = ROOT / "HISTORY.md"

MAX_TABLE_RUNS = 42  # roughly 7 days at 4-hour intervals
TREND_RUNS = 12      # roughly 2 days

LABELS = {
    3: "Very bullish", 2: "Bullish", 1: "Leaning bullish", 0: "Neutral / mixed",
    -1: "Leaning bearish", -2: "Bearish", -3: "Very bearish",
}


def main() -> None:
    rows = list(csv.DictReader(CSV_PATH.open()))
    if not rows:
        raise SystemExit("history/scores.csv has no data rows")

    commodities: "OrderedDict[str, None]" = OrderedDict()
    runs: "OrderedDict[str, dict]" = OrderedDict()  # ts -> {commodity: row}
    for r in rows:
        commodities.setdefault(r["commodity"], None)
        runs.setdefault(r["timestamp_utc"], {})[r["commodity"]] = r

    ids = list(commodities)
    timestamps = sorted(runs)  # ISO timestamps sort chronologically

    def fmt(ts: str, cid: str) -> str:
        r = runs[ts].get(cid)
        if r is None:
            return "·"
        s = int(r["score"])
        return f"+{s}" if s > 0 else str(s)

    lines = [
        "# Sentiment Score History",
        "",
        "Standardized 7-point scale: **-3** Very bearish · **-2** Bearish · "
        "**-1** Leaning bearish · **0** Neutral/mixed · **+1** Leaning bullish · "
        "**+2** Bullish · **+3** Very bullish.",
        "",
        "Source of truth: [`history/scores.csv`](history/scores.csv). "
        "Regenerate this file with `python3 scripts/render_history.py`. "
        "Full write-ups for every run live in [`reports/`](reports/).",
        "",
        "## Latest reading",
        "",
        "| Commodity | Score | Label | Trend (oldest → newest, last "
        f"{TREND_RUNS} runs) |",
        "|---|---|---|---|",
    ]

    latest_ts = timestamps[-1]
    trend_ts = timestamps[-TREND_RUNS:]
    for cid in ids:
        latest = runs[latest_ts].get(cid)
        score = fmt(latest_ts, cid)
        label = latest["label"] if latest else "—"
        trail = " → ".join(fmt(ts, cid) for ts in trend_ts if cid in runs[ts])
        lines.append(f"| {cid} | {score} | {label} | {trail} |")

    lines += [
        "",
        f"## Run-by-run scores (last {MAX_TABLE_RUNS} runs, newest first)",
        "",
        "| Run (UTC) | " + " | ".join(ids) + " |",
        "|---" * (len(ids) + 1) + "|",
    ]
    for ts in reversed(timestamps[-MAX_TABLE_RUNS:]):
        lines.append(f"| {ts} | " + " | ".join(fmt(ts, cid) for cid in ids) + " |")

    pairs_csv = ROOT / "history" / "pairs.csv"
    if pairs_csv.exists():
        prows = list(csv.DictReader(pairs_csv.open()))
        pids: "OrderedDict[str, None]" = OrderedDict()
        pruns: "OrderedDict[str, dict]" = OrderedDict()
        for r in prows:
            pids.setdefault(r["pair"], None)
            pruns.setdefault(r["timestamp_utc"], {})[r["pair"]] = int(r["diff"])

        def pfmt(ts: str, pid: str) -> str:
            d = pruns[ts].get(pid)
            if d is None:
                return "·"
            return f"+{d}" if d > 0 else str(d)

        pts = sorted(pruns)
        lines += [
            "",
            "## RV pair sentiment differentials (leg1 − leg2, "
            f"last {MAX_TABLE_RUNS} runs, newest first)",
            "",
            "Positive = news flow favors leg1 outperformance. Pairs defined "
            "in `config/commodities.yaml`; raw data in "
            "[`history/pairs.csv`](history/pairs.csv).",
            "",
            "| Run (UTC) | " + " | ".join(pids) + " |",
            "|---" * (len(pids) + 1) + "|",
        ]
        for ts in reversed(pts[-MAX_TABLE_RUNS:]):
            lines.append(f"| {ts} | " +
                         " | ".join(pfmt(ts, p) for p in pids) + " |")

    lines.append("")
    OUT_PATH.write_text("\n".join(lines))
    print(f"Wrote {OUT_PATH} ({len(timestamps)} runs, {len(ids)} commodities)")


if __name__ == "__main__":
    main()
