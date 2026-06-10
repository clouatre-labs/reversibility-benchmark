"""
Figure 3: Per-item verdict consistency heatmap.

Three horizontal strips (one per classifier) showing halt (blue) vs pass (orange)
for all 60 scenarios in order. All verdicts were consistent across 3 runs (std=0),
so each cell is the single modal verdict. Renders fig3-consistency.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv
import os

CONSISTENCY_CSV = 'experiments/aggregate/consistency.csv'

# Read consistency.csv -> {classifier: {scenario_id: verdict_mode}}
data = {}
with open(CONSISTENCY_CSV) as f:
    for row in csv.DictReader(f):
        clf = row['classifier']
        sid = row['scenario_id']
        verdict = row['verdict_mode']
        data.setdefault(clf, {})[sid] = verdict

CLASSIFIERS = ['A', 'B', 'C']
LABELS = ['A (multi-factor risk)', 'B (reversibility gate)', 'C (combined A OR B)']
scenario_ids = sorted(data['A'].keys())  # s001..s060
N = len(scenario_ids)

# Build matrix: 3 rows x 60 cols; halt=1, pass=0
matrix = np.zeros((3, N))
for r, clf in enumerate(CLASSIFIERS):
    for c, sid in enumerate(scenario_ids):
        matrix[r, c] = 1 if data[clf][sid] == 'halt' else 0

fig, ax = plt.subplots(figsize=(14, 2.8))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

cmap = matplotlib.colors.ListedColormap(['#DD8452', '#4C72B0'])  # pass=orange, halt=blue
ax.imshow(matrix, aspect='auto', cmap=cmap, vmin=0, vmax=1, interpolation='nearest')

ax.set_yticks(range(3))
ax.set_yticklabels(LABELS, fontsize=9)

# x-ticks every 10 scenarios
tick_positions = list(range(0, N, 10))
ax.set_xticks(tick_positions)
ax.set_xticklabels([scenario_ids[i] for i in tick_positions], fontsize=8, rotation=30, ha='right')

ax.set_xlabel('Scenario', fontsize=10)

halt_patch = mpatches.Patch(color='#4C72B0', label='Halt')
pass_patch = mpatches.Patch(color='#DD8452', label='Pass')
ax.legend(handles=[halt_patch, pass_patch], fontsize=9,
          loc='upper right', bbox_to_anchor=(1.0, 1.35), ncol=2)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/fig3-consistency.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig3-consistency.png')
