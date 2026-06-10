"""
Figure 3: Verdict disagreement -- scenarios where A and C diverge.

Reads corpus/scenarios.json and experiments/aggregate/consistency.csv directly.
Shows the 6 scenarios where A passed but C halted (B rescued), annotated by
true label. Colour encodes outcome type: correct halt (B caught a real miss)
vs false positive (B over-halted a reversible item, dragging C with it).
Renders fig3-verdict-disagreement.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv, json

# --- Load data ---
data = json.load(open('corpus/scenarios.json'))
scenarios = {s['id']: s for s in data['scenarios']}

rows = list(csv.DictReader(open('experiments/aggregate/consistency.csv')))
verdicts = {}
for r in rows:
    verdicts.setdefault(r['classifier'], {})[r['scenario_id']] = r['verdict_mode']

fc_rows = list(csv.DictReader(open('experiments/aggregate/failure-classifications.csv')))
# {(clf, sid): row}
fc = {(r['classifier'], r['scenario_id']): r for r in fc_rows}

# --- Identify disagreement scenarios: A=pass, C=halt ---
disagreements = []
for sid in sorted(scenarios.keys()):
    if verdicts['A'][sid] == 'pass' and verdicts['C'][sid] == 'halt':
        sc = scenarios[sid]
        c_row = fc.get(('C', sid), {})
        is_fp = c_row.get('false_positive', '0') == '1'
        disagreements.append({
            'sid': sid,
            'rev': sc['reversibility'],
            'risk': sc['risk_tier'],
            'fp': is_fp,   # True = B over-halted a reversible item
        })

# --- Layout: scatter with jitter, x=risk_tier, y=reversibility ---
REV_ORDER  = {'reversible': 0, 'bounded_reversible': 1, 'irreversible': 2}
RISK_ORDER = {'low': 0, 'medium': 1, 'high': 2}

fig, ax = plt.subplots(figsize=(7, 4.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Draw all 60 scenarios as light background dots first
for sid, sc in scenarios.items():
    rx = RISK_ORDER[sc['risk_tier']]
    ry = REV_ORDER[sc['reversibility']]
    ax.scatter(rx, ry, s=40, color='#cccccc', zorder=1, alpha=0.5)

# Overlay disagreement scenarios
for item in disagreements:
    rx = RISK_ORDER[item['risk']]
    ry = REV_ORDER[item['rev']]
    color = '#DD8452' if item['fp'] else '#4C72B0'
    marker = 'X' if item['fp'] else 'o'
    ax.scatter(rx, ry, s=160, color=color, marker=marker,
               zorder=3, edgecolors='#222222', linewidths=0.8)
    ax.annotate(item['sid'],
                xy=(rx, ry), xytext=(8, 6),
                textcoords='offset points',
                fontsize=7.5, color='#333333', zorder=4)

ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Low risk', 'Medium risk', 'High risk'], fontsize=10)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['Reversible', 'Bounded\nreversible', 'Irreversible'], fontsize=10)
ax.set_xlim(-0.6, 2.6)
ax.set_ylim(-0.6, 2.6)

# Grid lines aligned to corpus cell boundaries
for v in [0.5, 1.5]:
    ax.axvline(v, color='#dddddd', linewidth=0.8, zorder=0)
    ax.axhline(v, color='#dddddd', linewidth=0.8, zorder=0)

# Legend
patch_miss  = mpatches.Patch(color='#4C72B0', label='B rescued a true miss (A missed, C halts correctly)')
patch_fp    = mpatches.Patch(color='#DD8452', label='B false positive (reversible item; C over-halts)')
patch_bg    = mpatches.Patch(color='#cccccc', label='A and C agree (n=54)')
ax.legend(handles=[patch_miss, patch_fp, patch_bg],
          fontsize=8, loc='upper left', framealpha=0.9)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/fig3-verdict-disagreement.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig3-verdict-disagreement.png')
