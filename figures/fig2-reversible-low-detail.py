"""
Figure 2: Classifier comparison on the two divergent subgroups.

Two-panel grouped bar chart.
  Left panel:  reversible/low (n=12)  -- the false-positive stress test
  Right panel: irreversible/low (n=5) -- the Fisher test cell

Each panel shows halt rate per classifier (A, B, C) with 95% Wilson CI bars
and the item count labelled inside each bar.
Reads experiments/aggregate/consistency.csv and corpus/scenarios.json directly.
Renders fig2-reversible-low-detail.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv, json

# --- Wilson score 95% CI ---
def wilson_ci(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    margin = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return max(0.0, centre - margin), min(1.0, centre + margin)

# --- Load ---
scenarios = {s['id']: s for s in json.load(open('corpus/scenarios.json'))['scenarios']}
rows = list(csv.DictReader(open('experiments/aggregate/consistency.csv')))

CLFS = ['A', 'B', 'C']
COLORS = {'A': '#4C72B0', 'B': '#DD8452', 'C': '#55A868'}
CLF_LABELS = ['A\nmulti-factor', 'B\nrev. gate', 'C\ncombined']

cells = {}
for r in rows:
    sc = scenarios[r['scenario_id']]
    key = (sc['reversibility'], sc['risk_tier'], r['classifier'])
    if key not in cells:
        cells[key] = {'halt': 0, 'total': 0}
    cells[key]['total'] += 1
    if r['verdict_mode'] == 'halt':
        cells[key]['halt'] += 1

subgroups = [
    ('reversible', 'low', 'Reversible / low-risk\n(false-positive stress, n=12)'),
    ('irreversible', 'low', 'Irreversible / low-risk\n(Fisher test cell, n=5)'),
]

fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
fig.patch.set_facecolor('white')

x = np.arange(3)
width = 0.5

for ax, (rev, risk, title) in zip(axes, subgroups):
    ax.set_facecolor('white')
    halts, lows, highs = [], [], []
    ns = []
    for clf in CLFS:
        c = cells[(rev, risk, clf)]
        k, n = c['halt'], c['total']
        halts.append(k / n if n else 0)
        lo, hi = wilson_ci(k, n)
        lows.append(halts[-1] - lo)
        highs.append(hi - halts[-1])
        ns.append(n)

    bars = ax.bar(x, halts, width,
                  color=[COLORS[c] for c in CLFS],
                  yerr=[lows, highs],
                  error_kw={'elinewidth': 1.5, 'capsize': 5, 'ecolor': '#444444'},
                  zorder=3)

    for bar, rate, lo, hi, n in zip(bars, halts, lows, highs, ns):
        label = f'{rate:.0%}\n(n={n})'
        ci_top = rate + hi   # top of error whisker
        if rate >= 0.30:
            # label inside the bar, well below the top
            ax.text(bar.get_x() + bar.get_width() / 2,
                    rate - 0.07, label,
                    ha='center', va='top', fontsize=10,
                    color='white', fontweight='bold', zorder=4)
        else:
            # label above the CI cap so it never overlaps the whisker
            ax.text(bar.get_x() + bar.get_width() / 2,
                    ci_top + 0.04, label,
                    ha='center', va='bottom', fontsize=10,
                    color='#1a1a1a', fontweight='bold', zorder=4)

    ax.set_xticks(x)
    ax.set_xticklabels(CLF_LABELS, fontsize=10)
    ax.set_ylim(0, 1.18)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0%}'))
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title, fontsize=10, pad=8)

axes[0].set_ylabel('Halt rate (95% Wilson CI)', fontsize=11)

fig.suptitle('Classifier halt rates on the two divergent subgroups', fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig('figures/fig2-reversible-low-detail.png', dpi=300, bbox_inches='tight')
print('Wrote figures/fig2-reversible-low-detail.png')
