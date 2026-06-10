"""
Figure 2: Per-scenario verdict detail for reversible/low items (n=12).

The only subgroup where classifiers diverge. Each row is a scenario; columns
are classifiers A, B, C. Filled circle = halt, open circle = pass.
Scenarios sorted by A verdict then scenario ID.
Reads experiments/aggregate/consistency.csv and corpus/scenarios.json directly.
Renders fig2-reversible-low-detail.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import csv, json

# --- Load ---
data = json.load(open('corpus/scenarios.json'))
scenarios = {s['id']: s for s in data['scenarios']}
rows = list(csv.DictReader(open('experiments/aggregate/consistency.csv')))
verdicts = {}
for r in rows:
    verdicts.setdefault(r['classifier'], {})[r['scenario_id']] = r['verdict_mode']

# --- Filter reversible/low ---
sids = sorted(
    [sid for sid, sc in scenarios.items()
     if sc['reversibility'] == 'reversible' and sc['risk_tier'] == 'low'],
    key=lambda sid: (verdicts['A'][sid], sid)
)

CLFS = ['A', 'B', 'C']
COLORS = {'A': '#4C72B0', 'B': '#DD8452', 'C': '#55A868'}

# --- Plot ---
fig, ax = plt.subplots(figsize=(5, 6))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

n = len(sids)
y_positions = np.arange(n)

for xi, clf in enumerate(CLFS):
    for yi, sid in enumerate(sids):
        v = verdicts[clf][sid]
        if v == 'halt':
            ax.scatter(xi, yi, s=180, color=COLORS[clf],
                       zorder=3, edgecolors=COLORS[clf], linewidths=1.2)
        else:
            ax.scatter(xi, yi, s=180, facecolors='white',
                       edgecolors=COLORS[clf], linewidths=1.8, zorder=3)

# Row labels (scenario IDs)
ax.set_yticks(y_positions)
ax.set_yticklabels(sids, fontsize=9)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['A\n(multi-factor risk)', 'B\n(reversibility gate)', 'C\n(combined)'],
                   fontsize=9)
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.7, n - 0.3)

# Horizontal grid lines between rows
for y in y_positions:
    ax.axhline(y, color='#eeeeee', linewidth=0.8, zorder=0)

# Legend
halt_marker = mlines.Line2D([], [], color='#666666', marker='o', linestyle='None',
                             markersize=9, label='Halt', markerfacecolor='#666666')
pass_marker = mlines.Line2D([], [], color='#666666', marker='o', linestyle='None',
                             markersize=9, label='Pass', markerfacecolor='white',
                             markeredgewidth=1.8)
ax.legend(handles=[halt_marker, pass_marker], fontsize=9,
          loc='lower right', framealpha=0.9)

ax.set_title('Reversible / low-risk items (n=12)', fontsize=10, pad=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/fig2-reversible-low-detail.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig2-reversible-low-detail.png')
