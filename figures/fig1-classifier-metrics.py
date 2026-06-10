"""
Figure 1: Two-panel classifier comparison.

Panel A -- Halt rate with 95% Wilson CI for each classifier.
Panel B -- Low-risk + irreversible cell breakdown (li_halt vs li_pass, n=5),
           with Fisher p annotated above each bar.

Renders fig1-classifier-metrics.png alongside this script.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

CLASSIFIERS  = ['A\n(multi-factor risk)', 'B\n(reversibility gate)', 'C\n(combined A OR B)']
HALT_RATE    = [0.750, 0.967, 0.850]
HALT_CI_LOW  = [0.628, 0.886, 0.739]
HALT_CI_HIGH = [0.842, 0.991, 0.919]
LI_HALT      = [1, 5, 5]
LI_PASS      = [4, 0, 0]
FISHER_P     = [0.0747, 0.4921, 0.0020]
N_CELL       = 5

x = np.arange(len(CLASSIFIERS))

err_low  = [h - l for h, l in zip(HALT_RATE, HALT_CI_LOW)]
err_high = [h - l for h, l in zip(HALT_CI_HIGH, HALT_RATE)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
fig.patch.set_facecolor('white')

# --- Panel A: halt rate with CI ---
ax1.set_facecolor('white')
bars = ax1.bar(x, HALT_RATE, 0.5, color='#4C72B0', zorder=3)
ax1.errorbar(x, HALT_RATE,
             yerr=[err_low, err_high],
             fmt='none', color='#222222', capsize=5, linewidth=1.4, zorder=4)
ax1.set_xticks(x)
ax1.set_xticklabels(CLASSIFIERS, fontsize=10)
ax1.set_ylabel('Halt rate', fontsize=11)
ax1.set_ylim(0, 1.12)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0%}'))
ax1.set_title('(A) Halt rate with 95% CI', fontsize=11, pad=8)
ax1.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.6, zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# value labels above bars
for bar, v in zip(bars, HALT_RATE):
    ax1.text(bar.get_x() + bar.get_width() / 2,
             v + 0.03, f'{v:.1%}',
             ha='center', va='bottom', fontsize=9, color='#222222')

# --- Panel B: low+irrev cell ---
ax2.set_facecolor('white')
ax2.bar(x, LI_HALT, 0.5, label='Halt', color='#4C72B0', zorder=3)
ax2.bar(x, LI_PASS, 0.5, bottom=LI_HALT,
        label='Pass (missed)', color='#DD8452', zorder=3)

# count labels inside bars
for i, (h, p) in enumerate(zip(LI_HALT, LI_PASS)):
    if h > 0:
        ax2.text(i, h / 2, str(h), ha='center', va='center',
                 fontsize=12, fontweight='bold', color='white')
    if p > 0:
        ax2.text(i, h + p / 2, str(p), ha='center', va='center',
                 fontsize=12, fontweight='bold', color='white')

# Fisher p above each bar
for i, p in enumerate(FISHER_P):
    label = f'p={p:.4f}{"*" if p < 0.05 else ""}'
    ax2.text(i, N_CELL + 0.15, label,
             ha='center', va='bottom', fontsize=8, color='#333333')

ax2.set_xticks(x)
ax2.set_xticklabels(CLASSIFIERS, fontsize=10)
ax2.set_ylabel('Scenarios (n=5 total)', fontsize=11)
ax2.set_ylim(0, N_CELL + 0.9)
ax2.set_yticks(range(N_CELL + 1))
ax2.set_title('(B) Low-risk + irreversible cell', fontsize=11, pad=8)
ax2.legend(fontsize=9, loc='upper right')
ax2.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.6, zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout(pad=2.0)
plt.savefig('figures/fig1-classifier-metrics.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig1-classifier-metrics.png')
