#!/usr/bin/env python3
"""Render a sentiment report to a styled PDF.

Usage: python3 scripts/render_pdf.py [reports/<file>.md]
Defaults to the newest report in reports/. Writes reports/pdf/<name>.pdf.

Reads the report's standardized structure (dashboard table, "Biggest shifts",
RV pair matrix, catalyst calendar, per-commodity sections) plus
history/scores.csv for the trend sparklines, builds a print-styled HTML page,
and prints it to PDF with headless Chromium.
"""
import csv
import html
import re
import subprocess
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROMIUM = "/opt/pw-browsers/chromium"

# Diverging bearish↔bullish scale: red arm / neutral gray / green arm
# (finance convention). Red/green is the hardest pair for colorblind readers,
# so every chip also carries its numeric score and text label — color never
# works alone. (chip background, chip text)
SCORE_STYLE = {
    3: ("#0d5222", "#ffffff"), 2: ("#1f7a33", "#ffffff"), 1: ("#b5dfb9", "#0b0b0b"),
    0: ("#f0efec", "#0b0b0b"),
    -1: ("#f5c4c3", "#0b0b0b"), -2: ("#e34948", "#ffffff"), -3: ("#8f2726", "#ffffff"),
}


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def inline_md(s: str) -> str:
    """Convert the inline markdown used in reports: links, bold, italics."""
    s = esc(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def read_table(lines: list, i: int):
    """Consume a markdown table starting at lines[i]; return (rows, next_i)."""
    rows = []
    while i < len(lines) and lines[i].startswith("|"):
        cells = [c.strip() for c in lines[i].strip("|").split("|")]
        if not set("".join(cells)) <= {"-", " ", ":"}:
            rows.append(cells)
        i += 1
    return rows, i


def body_blocks(lines: list) -> list:
    """Split section body lines into ('table', rows) / ('p', text) blocks."""
    blocks, cur, i = [], [], 0
    while i < len(lines):
        if lines[i].startswith("|"):
            if cur:
                blocks.append(("p", " ".join(cur)))
                cur = []
            rows, i = read_table(lines, i)
            blocks.append(("table", rows))
            continue
        if lines[i].strip():
            cur.append(lines[i].strip())
        elif cur:
            blocks.append(("p", " ".join(cur)))
            cur = []
        i += 1
    if cur:
        blocks.append(("p", " ".join(cur)))
    return blocks


def parse_report(text: str) -> dict:
    lines = text.splitlines()
    doc = {"title": "", "preamble": "", "dashboard": [], "sections": []}
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# ") and not doc["title"]:
            doc["title"] = ln[2:].strip()
        elif ln.startswith("*") and not doc["preamble"] and not doc["dashboard"]:
            para = []
            while i < len(lines) and lines[i].strip():
                para.append(lines[i].strip())
                i += 1
            doc["preamble"] = " ".join(para).strip("*").strip()
            continue
        elif ln.startswith("|") and not doc["dashboard"]:
            doc["dashboard"], i = read_table(lines, i)
            continue
        elif ln.startswith("## "):
            heading = ln[3:].strip()
            i += 1
            body = []
            while i < len(lines) and not lines[i].startswith("## ") \
                    and lines[i].strip() != "---":
                body.append(lines[i])
                i += 1
            doc["sections"].append({"heading": heading,
                                    "blocks": body_blocks(body)})
            continue
        i += 1
    return doc


def score_of(cell: str) -> int:
    m = re.search(r"[+-]?\d", cell)
    return int(m.group()) if m else 0


def chip(score: int, label: str) -> str:
    bg, fg = SCORE_STYLE.get(max(-3, min(3, score)), SCORE_STYLE[0])
    num = f"+{score}" if score > 0 else str(score)
    return (f'<span class="chip" style="background:{bg};color:{fg}">'
            f"{num}&ensp;{esc(label)}</span>")


def crowd_badge(cell: str) -> str:
    m = re.search(r"\d", cell)
    if not m:
        return esc(cell)
    n = int(m.group())
    dots = "●" * n + "○" * (3 - n)
    warn = " crowd-hot" if n >= 3 else ""
    return f'<span class="crowd{warn}" title="crowdedness {n}/3">{dots}&thinsp;{n}</span>'


def sparkline(scores: list) -> str:
    """Inline SVG trend of scores (-3..+3), oldest → newest."""
    w, h, pad = 200, 48, 8
    n = max(len(scores), 2)
    xs = [pad + i * (w - 2 * pad) / (n - 1) for i in range(len(scores))]
    ys = [h / 2 - s * (h / 2 - pad) / 3 for s in scores]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    dots = []
    for j, (x, y, s) in enumerate(zip(xs, ys, scores)):
        bg, _ = SCORE_STYLE[max(-3, min(3, s))]
        r = 4.5 if j == len(scores) - 1 else 3
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{bg}" '
                    f'stroke="#fcfcfb" stroke-width="1.5"/>')
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<line x1="{pad}" y1="{h/2}" x2="{w-pad}" y2="{h/2}" '
            f'stroke="#e1e0d9" stroke-width="1"/>'
            f'<polyline points="{pts}" fill="none" stroke="#c3c2b7" stroke-width="2" '
            f'stroke-linejoin="round" stroke-linecap="round"/>{"".join(dots)}</svg>')


def load_history() -> "OrderedDict[str, list]":
    hist: "OrderedDict[str, list]" = OrderedDict()
    p = ROOT / "history" / "scores.csv"
    if p.exists():
        for r in csv.DictReader(p.open()):
            hist.setdefault(r["commodity"], []).append(int(r["score"]))
    return hist


CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
       color: #0b0b0b; background: #fcfcfb; font-size: 10.5px; line-height: 1.55; }
a { color: #1c5cab; text-decoration: none; }
header { border-bottom: 3px solid #0b0b0b; padding-bottom: 12px; margin-bottom: 16px; }
.kicker { font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase;
          color: #52514e; margin-bottom: 4px; }
h1 { font-size: 24px; font-weight: 700; letter-spacing: -0.01em; }
.stamp { color: #898781; margin-top: 4px; font-size: 11px; }
.preamble { color: #52514e; font-style: italic; margin-bottom: 14px; }
table.dash, table.generic { width: 100%; border-collapse: collapse; margin-bottom: 4px; }
table.dash th, table.generic th { text-align: left; font-size: 9px; letter-spacing: 0.08em;
    text-transform: uppercase; color: #898781; padding: 0 8px 6px 0;
    border-bottom: 1.5px solid #c3c2b7; }
table.dash td, table.generic td { padding: 7px 8px 7px 0; border-bottom: 1px solid #e1e0d9;
    vertical-align: middle; }
table.generic { margin-bottom: 16px; }
table.generic td { padding: 5px 8px 5px 0; color: #1c1c1a; }
table.dash td.name { font-weight: 600; white-space: nowrap; }
table.dash td.delta { color: #52514e; white-space: nowrap; }
table.dash td.driver { color: #52514e; }
.chip { display: inline-block; border-radius: 4px; padding: 2.5px 9px;
        font-weight: 600; font-size: 10px; white-space: nowrap; }
.crowd { color: #52514e; letter-spacing: 1px; white-space: nowrap; }
.crowd-hot { color: #b26a00; font-weight: 700; }
.legend { color: #898781; font-size: 9px; margin: 6px 0 16px; }
.callout { background: #f5f4f1; border-left: 4px solid #0b0b0b; border-radius: 4px;
           padding: 11px 14px; margin-bottom: 18px; }
.callout .cap { font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase;
                color: #52514e; font-weight: 700; margin-bottom: 4px; }
h2.block { font-size: 13px; margin: 4px 0 8px; }
table.trend { width: 100%; border-collapse: collapse; margin-bottom: 18px; }
table.trend td { padding: 3px 10px 3px 0; border-bottom: 1px solid #efeee9;
                 vertical-align: middle; }
table.trend td.name { font-weight: 600; white-space: nowrap; width: 1%; }
.section { break-inside: avoid; border-left: 4px solid var(--accent, #c3c2b7);
           padding: 2px 0 2px 12px; margin-bottom: 14px; }
.section h3 { font-size: 13px; margin-bottom: 5px; }
.section h3 .chip { font-size: 9.5px; margin-left: 6px; vertical-align: 1px; }
.section h3 .crowd { font-size: 10px; margin-left: 8px; }
.section p { margin-bottom: 5px; color: #1c1c1a; }
.section p strong:first-child { color: #0b0b0b; }
.blockwrap { break-inside: avoid; }
footer { margin-top: 18px; padding-top: 8px; border-top: 1px solid #e1e0d9;
         color: #898781; font-size: 9px; }
"""


def generic_table(rows: list) -> str:
    head, *body = rows
    out = ["<table class='generic'><tr>" +
           "".join(f"<th>{inline_md(h)}</th>" for h in head) + "</tr>"]
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in r) + "</tr>")
    out.append("</table>")
    return "".join(out)


def build_html(doc: dict, hist: "OrderedDict[str, list]") -> str:
    rows = doc["dashboard"][1:]
    dash = ["<table class='dash'><tr><th>Commodity</th><th>Sentiment</th>"
            "<th>Crowd</th><th>&Delta; vs last</th><th>One-line driver</th></tr>"]
    for r in rows:
        # Commodity | Sentiment | Score | Crowd | Δ | driver (older reports
        # lack Crowd; pad)
        if len(r) == 5:
            r = r[:3] + ["—"] + r[3:]
        name, label, sc, crowd, delta, driver = (
            r[0], r[1], score_of(r[2]), r[3], r[4], r[5])
        dash.append(
            f"<tr><td class='name'>{esc(name)}</td><td>{chip(sc, label)}</td>"
            f"<td>{crowd_badge(crowd)}</td><td class='delta'>{esc(delta)}</td>"
            f"<td class='driver'>{inline_md(driver)}</td></tr>")
    dash.append("</table>")

    trend_rows = []
    for cid, ss in hist.items():
        trail = " &rarr; ".join((f"+{s}" if s > 0 else str(s)) for s in ss[-12:])
        trend_rows.append(f"<tr><td class='name'>{esc(cid)}</td>"
                          f"<td>{sparkline(ss[-12:])}</td>"
                          f"<td style='color:#52514e'>{trail}</td></tr>")

    shifts_html, block_html, section_html = "", [], []
    for s in doc["sections"]:
        m = re.match(r"(.+?)\s+—\s+(.+?)\s*\(([+-]?\d)\)(?:\s*·\s*crowd\s*(\d))?",
                     s["heading"])
        if m:  # per-commodity section
            name, label, sc = m.group(1), m.group(2), int(m.group(3))
            accent, _ = SCORE_STYLE[max(-3, min(3, sc))]
            title = f"{esc(name)} {chip(sc, label)}"
            if m.group(4):
                title += f" {crowd_badge(m.group(4))}"
            paras = "".join(
                f"<p>{inline_md(b[1])}</p>" if b[0] == "p" else generic_table(b[1])
                for b in s["blocks"])
            section_html.append(f"<div class='section' style='--accent:{accent}'>"
                                f"<h3>{title}</h3>{paras}</div>")
        elif s["heading"].lower().startswith("biggest shifts"):
            text = " ".join(b[1] for b in s["blocks"] if b[0] == "p")
            shifts_html = (f"<div class='callout'><div class='cap'>Biggest shifts"
                           f"</div>{inline_md(text)}</div>")
        else:  # generic block section (pair matrix, calendar, …)
            parts = [f"<h2 class='block'>{inline_md(s['heading'])}</h2>"]
            for b in s["blocks"]:
                parts.append(f"<p class='legend'>{inline_md(b[1])}</p>"
                             if b[0] == "p" else generic_table(b[1]))
            block_html.append("<div class='blockwrap'>" + "".join(parts) + "</div>")

    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
<header>
  <div class="kicker">TPRV &middot; Commodities Sentiment Monitor &middot; RV desk edition</div>
  <h1>Commodities Sentiment Report</h1>
  <div class="stamp">{esc(doc['title'].split('—')[-1].strip())}</div>
</header>
<p class="preamble">{inline_md(doc['preamble'])}</p>
{''.join(dash)}
<div class="legend">Direction: &minus;3 Very bearish &rarr; +3 Very bullish.
Crowd: 0 two-sided &rarr; 3 crowded &amp; uniform (contrarian risk). Sentiment
reflects the tone of current news and trader coverage about the price outlook,
not the last price move.</div>
{shifts_html}
{''.join(block_html)}
<h2 class="block">Score history (oldest &rarr; newest)</h2>
<table class="trend">{''.join(trend_rows)}</table>
{''.join(section_html)}
<footer>Generated by the TPRV commodities sentiment monitor &middot; methodology
in MONITOR.md &middot; sources linked inline &middot; full archive in reports/,
history/scores.csv and history/pairs.csv &middot; internal research synthesis,
not investment advice</footer>
</body></html>"""


def main() -> None:
    if len(sys.argv) > 1:
        report = Path(sys.argv[1])
    else:
        report = sorted((ROOT / "reports").glob("*.md"))[-1]
    doc = parse_report(report.read_text())
    out_html = build_html(doc, load_history())
    out_dir = ROOT / "reports" / "pdf"
    out_dir.mkdir(exist_ok=True)
    out_pdf = out_dir / (report.stem + ".pdf")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(out_html)
        tmp = f.name
    subprocess.run(
        [CHROMIUM, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", f"file://{tmp}"],
        check=True, capture_output=True)
    print(f"Wrote {out_pdf}")


if __name__ == "__main__":
    main()
