"""Figure: B2 precision-recall curve across confidence thresholds.

Reads:  experiments/aggregate/b2-precision-recall.csv
Writes: figures/b2-pr-curve.png
"""

import csv
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parent.parent
PR_CSV = REPO_ROOT / "experiments" / "aggregate" / "b2-precision-recall.csv"
OUT_PNG = REPO_ROOT / "figures" / "b2-pr-curve.png"


def main() -> None:
    if not PR_CSV.exists():
        print(f"ERROR: {PR_CSV} not found; run classify.py --classifier B2 then score.py first")
        return

    thresholds = []
    precisions = []
    recalls = []
    f1s = []

    with open(PR_CSV) as f:
        for row in csv.DictReader(f):
            thresholds.append(int(row["threshold"]))
            precisions.append(float(row["precision"]))
            recalls.append(float(row["recall"]))
            f1s.append(float(row["f1"]))

    if not thresholds:
        print("ERROR: b2-precision-recall.csv is empty")
        return

    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor("white")

    ax.plot(recalls, precisions, marker="o", color="#4C72B0", linewidth=1.5, zorder=2)

    for t, r, p in zip(thresholds, recalls, precisions):
        ax.annotate(
            f"t={t}",
            xy=(r, p),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=9,
            color="#333333",
        )

    ax.set_xlabel("Recall", fontsize=11)
    ax.set_ylabel("Precision", fontsize=11)
    ax.set_title("Classifier B2: Precision-Recall by Confidence Threshold", fontsize=11)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_facecolor("white")

    plt.tight_layout()
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
