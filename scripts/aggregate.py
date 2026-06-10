"""Aggregate scoring results from score.py into summary CSVs.

Reads:  experiments/aggregate/summary.csv
        experiments/aggregate/consistency.csv
        experiments/aggregate/failure-classifications.csv
        experiments/aggregate/b2-precision-recall.csv  (if present)
Writes: no additional files; this script is a thin wrapper that validates
        and prints aggregate output already produced by score.py.

For B2 aggregation, score.py already writes b2-precision-recall.csv directly.
This script reads that CSV and prints a formatted operating-point table.
"""

import csv
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
AGGREGATE_DIR = REPO_ROOT / "experiments" / "aggregate"


def print_summary() -> None:
    path = AGGREGATE_DIR / "summary.csv"
    if not path.exists():
        print(f"ERROR: {path} not found; run score.py first", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        rows = list(csv.DictReader(f))
    print("=== Classifier Summary ===")
    for row in rows:
        clf = row["classifier"]
        halt = float(row["halt_rate"])
        miss = float(row["miss_rate"])
        fpr = float(row["false_positive_rate"])
        fp = row["fisher_p_value"]
        cp = row.get("corrected_fisher_p", "n/a")
        print(
            f"  {clf}  halt={halt:.1%}  miss={miss:.1%}  fp_rate={fpr:.1%}"
            f"  fisher_p={fp}  corrected_p={cp}"
        )


def print_b2_pr() -> None:
    path = AGGREGATE_DIR / "b2-precision-recall.csv"
    if not path.exists():
        print(
            "  (B2 precision-recall CSV not found; run classify.py --classifier B2 then score.py)"
        )
        return
    with open(path) as f:
        rows = list(csv.DictReader(f))
    print("=== B2 Precision-Recall Sweep ===")
    print(
        f"  {'threshold':>9}  {'precision':>9}  {'recall':>6}  {'f1':>6}  {'halt_rate':>9}"
    )
    for row in rows:
        t = row["threshold"]
        prec = float(row["precision"])
        rec = float(row["recall"])
        f1 = float(row["f1"])
        hr = float(row["halt_rate"])
        print(f"  {t:>9}  {prec:>9.3f}  {rec:>6.3f}  {f1:>6.3f}  {hr:>9.3f}")


def main() -> None:
    print_summary()
    print()
    print_b2_pr()


if __name__ == "__main__":
    main()
