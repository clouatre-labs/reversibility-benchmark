"""
Figure 2: Low-risk + irreversible cell breakdown.

Stacked bar showing li_halt vs li_pass counts for each classifier in the headline
test cell (low risk + irreversible, n=5). Renders fig2-low-irrev-cell.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

CLASSIFIERS = ['A\n(multi-factor risk)', 'B\n(reversibility gate)', 'C\n(combined A OR B)']
LI_HALT = [1, 5, 5]
LI_PASS = [4, 0, 0]
N = 5

x = np.arange(len(CLASSIFIERS))
width = 0.45

fig, ax = plt.subplots(figsize=(6, 4.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

bars_halt = ax.bar(x, LI_HALT, width, label='Halted (correct)', color='#4C72B0', zorder=3)
bars_pass = ax.bar(x, LI_PASS, width, bottom=LI_HALT,
                   label='Passed (missed)', color='#DD8452', zorder=3)

# Annotate counts inside bars
for i, (h, p) in enumerate(zip(LI_HALT, LI_PASS)):
    if h > 0:
        ax.text(i, h / 2, str(h), ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')
    if p > 0:
        ax.text(i, h + p / 2, str(p), ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')

ax.set_xticks(x)
ax.set_xticklabels(CLASSIFIERS, fontsize=10)
ax.set_ylabel('Scenarios (n=5 total)', fontsize=11)
ax.set_ylim(0, N + 0.8)
ax.set_yticks(range(N + 1))
ax.legend(fontsize=9, loc='upper right')
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.6, zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Fisher p annotations
fisher_p = [0.0747, 0.4921, 0.0020]
for i, p in enumerate(fisher_p):
    label = f'p={p:.4f}{"*" if p < 0.05 else ""}'
    ax.text(i, N + 0.35, label, ha='center', va='bottom', fontsize=8, color='#333333')

plt.tight_layout()
plt.savefig('figures/fig2-low-irrev-cell.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig2-low-irrev-cell.png')
