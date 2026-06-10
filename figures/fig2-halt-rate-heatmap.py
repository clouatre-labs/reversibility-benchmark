"""
Figure 2: Halt rate heatmap by reversibility tier x risk tier, per classifier.

Reads corpus/scenarios.json and experiments/aggregate/consistency.csv directly.
Rows = classifiers (A, B, C). Columns = subgroups (reversibility x risk tier).
Cell colour = halt rate within that subgroup; cell text = rate + item count.
Empty subgroups (n=0) are left blank.
Renders fig2-halt-rate-heatmap.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import csv, json
from collections import defaultdict

# --- Load data ---
data = json.load(open('corpus/scenarios.json'))
scenarios = {s['id']: s for s in data['scenarios']}

rows = list(csv.DictReader(open('experiments/aggregate/consistency.csv')))
verdicts = {}
for r in rows:
    verdicts.setdefault(r['classifier'], {})[r['scenario_id']] = r['verdict_mode']

# --- Compute halt rates per (clf, reversibility, risk_tier) ---
REVS  = ['reversible', 'bounded_reversible', 'irreversible']
RISKS = ['low', 'medium', 'high']
CLFS  = ['A', 'B', 'C']

# column labels: rev/risk pairs that have at least one item
col_keys = [(rev, risk) for rev in REVS for risk in RISKS]
occupied = []
for key in col_keys:
    rev, risk = key
    n = sum(1 for sc in scenarios.values()
            if sc['reversibility'] == rev and sc['risk_tier'] == risk)
    if n > 0:
        occupied.append((key, n))

# Build matrix: rows=classifiers, cols=occupied subgroups
matrix = np.full((len(CLFS), len(occupied)), np.nan)
for ci, clf in enumerate(CLFS):
    for ki, ((rev, risk), n) in enumerate(occupied):
        halts = sum(
            1 for sid, sc in scenarios.items()
            if sc['reversibility'] == rev and sc['risk_tier'] == risk
            and verdicts[clf][sid] == 'halt'
        )
        matrix[ci, ki] = halts / n

# --- Plot ---
col_labels = []
col_ns = []
for (rev, risk), n in occupied:
    rev_short = {'reversible': 'rev', 'bounded_reversible': 'b_rev', 'irreversible': 'irrev'}[rev]
    col_labels.append(f'{rev_short}\n{risk}')
    col_ns.append(n)

fig, ax = plt.subplots(figsize=(10, 3.2))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

cmap = mcolors.LinearSegmentedColormap.from_list(
    'rg', ['#f7f7f7', '#4393c3', '#2166ac'], N=256)

im = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect='auto')

# Cell annotations
for ci in range(len(CLFS)):
    for ki in range(len(occupied)):
        v = matrix[ci, ki]
        text_color = 'white' if v > 0.6 else '#222222'
        ax.text(ki, ci, f'{v:.0%}\n(n={col_ns[ki]})',
                ha='center', va='center', fontsize=8,
                color=text_color, fontweight='bold' if v == 1.0 or v == 0.0 else 'normal')

ax.set_xticks(range(len(occupied)))
ax.set_xticklabels(col_labels, fontsize=9)
ax.set_yticks(range(len(CLFS)))
ax.set_yticklabels(['A (multi-factor risk)', 'B (reversibility gate)', 'C (combined A OR B)'],
                   fontsize=9)

# Colorbar
cbar = plt.colorbar(im, ax=ax, orientation='vertical', fraction=0.03, pad=0.02)
cbar.set_label('Halt rate', fontsize=9)
cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0%}'))

# Separator lines between reversibility groups
group_sizes = {}
for (rev, risk), n in occupied:
    group_sizes[rev] = group_sizes.get(rev, 0) + 1
boundaries = []
count = 0
for rev in REVS:
    count += group_sizes.get(rev, 0)
    boundaries.append(count)
for b in boundaries[:-1]:
    ax.axvline(b - 0.5, color='#888888', linewidth=1.2, linestyle='--')

# Group labels above
group_starts = {}
pos = 0
for rev in REVS:
    sz = group_sizes.get(rev, 0)
    if sz:
        group_starts[rev] = pos + (sz - 1) / 2
        pos += sz
rev_display = {'reversible': 'Reversible', 'bounded_reversible': 'Bounded reversible',
               'irreversible': 'Irreversible'}
for rev, xpos in group_starts.items():
    ax.text(xpos, -0.9, rev_display[rev],
            ha='center', va='top', fontsize=9, fontstyle='italic',
            transform=ax.get_xaxis_transform())

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(length=0)

plt.tight_layout()
plt.savefig('figures/fig2-halt-rate-heatmap.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig2-halt-rate-heatmap.png')
