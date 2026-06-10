"""
Figure 1: Classifier metrics bar chart.

Grouped bar chart showing halt rate, miss rate (irreversible), and false-positive rate
for each of the three classifiers. Renders fig1-classifier-metrics.png alongside this script.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

CLASSIFIERS = ['A\n(multi-factor risk)', 'B\n(reversibility gate)', 'C\n(combined A OR B)']

HALT_RATE        = [0.750, 0.967, 0.850]
MISS_RATE        = [0.138, 0.000, 0.000]
FP_RATE          = [0.645, 0.936, 0.710]

HALT_CI_LOW      = [0.628, 0.886, 0.739]
HALT_CI_HIGH     = [0.842, 0.991, 0.919]

# 95% CI as asymmetric errors for halt rate
halt_err_low  = [h - l for h, l in zip(HALT_RATE, HALT_CI_LOW)]
halt_err_high = [h - l for h, l in zip(HALT_CI_HIGH, HALT_RATE)]

x = np.arange(len(CLASSIFIERS))
width = 0.25

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

bars_halt = ax.bar(x - width, HALT_RATE, width,
                   label='Halt rate', color='#4C72B0', zorder=3)
ax.errorbar(x - width, HALT_RATE,
            yerr=[halt_err_low, halt_err_high],
            fmt='none', color='#222222', capsize=4, linewidth=1.2, zorder=4)

bars_miss = ax.bar(x, MISS_RATE, width,
                   label='Miss rate (irreversible)', color='#DD8452', zorder=3)

bars_fp = ax.bar(x + width, FP_RATE, width,
                 label='False-positive rate', color='#55A868', zorder=3)

ax.set_xticks(x)
ax.set_xticklabels(CLASSIFIERS, fontsize=10)
ax.set_ylabel('Rate', fontsize=11)
ax.set_ylim(0, 1.12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0%}'))
ax.legend(fontsize=9, loc='upper right')
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.6, zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/fig1-classifier-metrics.png', dpi=150, bbox_inches='tight')
print('Wrote figures/fig1-classifier-metrics.png')
