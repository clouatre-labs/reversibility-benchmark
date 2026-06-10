"""
Figure 1: Halt rate with 95% Wilson CI per classifier.

Bar chart of halt rate for Classifiers A, B, C with asymmetric 95% Wilson CI
error bars. Values labelled above each bar. Renders fig1-classifier-metrics.png.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

CLASSIFIERS  = ['A\n(multi-factor risk)', 'B\n(reversibility gate)', 'C\n(combined A OR B)']
HALT_RATE    = [0.750, 0.967, 0.850]
HALT_CI_LOW  = [0.628, 0.886, 0.739]
HALT_CI_HIGH = [0.842, 0.991, 0.919]

x = np.arange(len(CLASSIFIERS))
err_low  = [h - l for h, l in zip(HALT_RATE, HALT_CI_LOW)]
err_high = [h - l for h, l in zip(HALT_CI_HIGH, HALT_RATE)]

fig, ax = plt.subplots(figsize=(6, 4.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

bars = ax.bar(x, HALT_RATE, 0.5, color='#4C72B0', zorder=3)
ax.errorbar(x, HALT_RATE,
            yerr=[err_low, err_high],
            fmt='none', color='#222222', capsize=6, linewidth=1.5, zorder=4)

for bar, v in zip(bars, HALT_RATE):
    ax.text(bar.get_x() + bar.get_width() / 2,
            v + 0.035, f'{v:.1%}',
            ha='center', va='bottom', fontsize=10, color='#222222')

ax.set_xticks(x)
ax.set_xticklabels(CLASSIFIERS, fontsize=10)
ax.set_ylabel('Halt rate (95% CI)', fontsize=11)
ax.set_ylim(0, 1.12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0%}'))
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.6, zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/fig1-classifier-metrics.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig1-classifier-metrics.png')
