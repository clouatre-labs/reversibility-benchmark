"""
Figure 1: Halt rate heatmap -- reversibility tier x risk tier, one panel per classifier.

3-panel heatmap (A, B, C). Rows = reversibility tier, columns = risk tier.
Cell text: halt_rate% (n=N). Empty cells shown in light grey.
Reads experiments/aggregate/consistency.csv and corpus/scenarios.json directly.
Renders fig1-halt-by-reversibility.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import csv, json
from collections import defaultdict

# --- Load ---
scenarios = {s['id']: s for s in json.load(open('corpus/scenarios.json'))['scenarios']}
rows = list(csv.DictReader(open('experiments/aggregate/consistency.csv')))

REVS = ['reversible', 'bounded_reversible', 'irreversible']
RISKS = ['low', 'medium', 'high']
CLFS = ['A', 'B', 'C']
CLF_LABELS = {
    'A': 'Classifier A\n(multi-factor risk)',
    'B': 'Classifier B\n(reversibility gate)',
    'C': 'Classifier C\n(combined)',
}
REV_LABELS = ['Reversible', 'Bounded\nreversible', 'Irreversible']
RISK_LABELS = ['Low', 'Medium', 'High']

cells = {}
for r in rows:
    sc = scenarios[r['scenario_id']]
    key = (sc['reversibility'], sc['risk_tier'], r['classifier'])
    if key not in cells:
        cells[key] = {'halt': 0, 'total': 0}
    cells[key]['total'] += 1
    if r['verdict_mode'] == 'halt':
        cells[key]['halt'] += 1

# Build 3D array: [clf, rev, risk]
rates = np.full((3, 3, 3), np.nan)
counts = np.zeros((3, 3), dtype=int)
for ri, rev in enumerate(REVS):
    for ki, risk in enumerate(RISKS):
        n = cells.get((rev, risk, 'A'), {}).get('total', 0)
        counts[ri, ki] = n
        for ci, clf in enumerate(CLFS):
            c = cells.get((rev, risk, clf), {'halt': 0, 'total': 0})
            if c['total'] > 0:
                rates[ci, ri, ki] = c['halt'] / c['total']

# Colormap: white=0%, dark blue=100%
cmap = mcolors.LinearSegmentedColormap.from_list(
    'halt', ['#f7fbff', '#4C72B0'], N=256
)

fig, axes = plt.subplots(1, 3, figsize=(11, 4), sharey=True)
fig.patch.set_facecolor('white')

for ci, (ax, clf) in enumerate(zip(axes, CLFS)):
    mat = rates[ci]  # shape (3 rev, 3 risk)
    # Mask NaN cells
    masked = np.ma.masked_invalid(mat)
    im = ax.imshow(masked, vmin=0, vmax=1, cmap=cmap, aspect='auto')

    # Grey out empty cells
    for ri in range(3):
        for ki in range(3):
            if np.isnan(mat[ri, ki]):
                ax.add_patch(plt.Rectangle(
                    (ki - 0.5, ri - 0.5), 1, 1,
                    facecolor='#e8e8e8', zorder=1
                ))

    # Cell annotations
    for ri in range(3):
        for ki in range(3):
            n = counts[ri, ki]
            if n == 0:
                ax.text(ki, ri, 'n/a', ha='center', va='center',
                        fontsize=9, color='#999999', zorder=2)
            else:
                rate = mat[ri, ki]
                pct = f'{rate:.0%}'
                # Dark text on light cells, white on dark
                text_color = 'white' if rate > 0.55 else '#1a1a1a'
                ax.text(ki, ri, f'{pct}\n(n={n})', ha='center', va='center',
                        fontsize=9, fontweight='bold', color=text_color, zorder=2)

    ax.set_xticks(range(3))
    ax.set_xticklabels(RISK_LABELS, fontsize=10)
    ax.set_xlabel('Risk tier', fontsize=10)
    ax.set_title(CLF_LABELS[clf], fontsize=10, pad=8)

    if ci == 0:
        ax.set_yticks(range(3))
        ax.set_yticklabels(REV_LABELS, fontsize=10)
        ax.set_ylabel('Reversibility tier', fontsize=10)

    # Box around the Fisher test cell (irreversible/low = row 2, col 0)
    ax.add_patch(plt.Rectangle(
        (-0.5, 1.5), 1, 1,
        fill=False, edgecolor='#e05c00', linewidth=2.0, zorder=3
    ))

# Colorbar
cbar = fig.colorbar(im, ax=axes[-1], fraction=0.046, pad=0.04)
cbar.set_label('Halt rate', fontsize=10)
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
cbar.set_ticklabels(['0%', '25%', '50%', '75%', '100%'])

fig.suptitle('Halt rate by reversibility x risk tier (orange box = Fisher test cell)',
             fontsize=11, y=1.02)

plt.tight_layout()
plt.savefig('figures/fig1-halt-by-reversibility.png', dpi=300, bbox_inches='tight')
print('Wrote figures/fig1-halt-by-reversibility.png')
