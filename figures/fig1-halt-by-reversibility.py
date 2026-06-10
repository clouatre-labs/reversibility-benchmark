"""
Figure 1: Halt rate by reversibility tier per classifier.

Grouped bar chart. X-axis: reversibility tier (reversible, bounded reversible,
irreversible). Three bars per group, one per classifier (A, B, C).
Values labelled inside or above each bar. No CI bars.
Reads experiments/aggregate/consistency.csv and corpus/scenarios.json directly.
Renders fig1-halt-by-reversibility.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv, json

# --- Load ---
data = json.load(open('corpus/scenarios.json'))
scenarios = {s['id']: s for s in data['scenarios']}
rows = list(csv.DictReader(open('experiments/aggregate/consistency.csv')))
verdicts = {}
for r in rows:
    verdicts.setdefault(r['classifier'], {})[r['scenario_id']] = r['verdict_mode']

REVS = ['reversible', 'bounded_reversible', 'irreversible']
CLFS = ['A', 'B', 'C']
COLORS = {'A': '#4C72B0', 'B': '#DD8452', 'C': '#55A868'}

rates = {}
counts = {}
for rev in REVS:
    sids = [sid for sid, sc in scenarios.items() if sc['reversibility'] == rev]
    counts[rev] = len(sids)
    for clf in CLFS:
        h = sum(1 for sid in sids if verdicts[clf][sid] == 'halt')
        rates[(clf, rev)] = h / len(sids)

# --- Plot ---
x = np.arange(len(REVS))
width = 0.22
offsets = {'A': -width, 'B': 0, 'C': width}

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

for clf in CLFS:
    vals = [rates[(clf, rev)] for rev in REVS]
    bars = ax.bar(x + offsets[clf], vals, width,
                  label=f'Classifier {clf}', color=COLORS[clf], zorder=3)
    for bar, v in zip(bars, vals):
        label = f'{v:.0%}'
        if v >= 0.15:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    v - 0.05, label,
                    ha='center', va='top', fontsize=9,
                    color='white', fontweight='bold')
        else:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    v + 0.02, label,
                    ha='center', va='bottom', fontsize=9,
                    color='#333333', fontweight='bold')

# X-axis labels with item counts
xlabels = [
    f'Reversible\n(n={counts["reversible"]})',
    f'Bounded reversible\n(n={counts["bounded_reversible"]})',
    f'Irreversible\n(n={counts["irreversible"]})',
]
ax.set_xticks(x)
ax.set_xticklabels(xlabels, fontsize=10)
ax.set_ylabel('Halt rate', fontsize=11)
ax.set_ylim(0, 1.12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0%}'))
ax.legend(fontsize=10, loc='upper left')
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5, zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/fig1-halt-by-reversibility.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig1-halt-by-reversibility.png')
