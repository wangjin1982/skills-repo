import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Wedge
import matplotlib.patheffects as path_effects

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=300)
ax.set_xlim(-10, 10)
ax.set_ylim(-6, 6)
ax.set_aspect('equal')
ax.axis('off')

# Color palette
DEEP_BLUE = '#1a365d'
RADIANT_ORANGE = '#ed8936'
NEUTRAL_GRAY = '#718096'
LIGHT_GRAY = '#e2e8f0'
WHITE = '#ffffff'
RED_WARNING = '#e53e3e'
GREEN_SUCCESS = '#38a169'

# Background
ax.set_facecolor('#fafafa')
fig.patch.set_facecolor('#fafafa')

# Concept: The KPI Trap - misaligned metrics leading to failure

# Top: Strategy (What we want)
strategy_box = Rectangle((-4, 4.2), 8, 1.6,
                        facecolor=DEEP_BLUE,
                        edgecolor='none',
                        alpha=0.9,
                        zorder=10,
                        )
ax.add_patch(strategy_box)

ax.text(0, 5.2,
       'STRATEGIC GOAL',
       ha='center',
       fontsize=11,
       fontweight='bold',
       color=WHITE,
       fontfamily='sans-serif',
       zorder=11)

ax.text(0, 4.65,
       'Sustainable Growth',
       ha='center',
       fontsize=9,
       color=WHITE,
       fontfamily='sans-serif',
       zorder=11)

# Middle Left: Wrong Metrics (The Trap)
trap_box = Rectangle((-7.5, 1.5), 6, 2.5,
                   facecolor=RED_WARNING,
                   edgecolor='none',
                   alpha=0.85,
                   zorder=8,
                   )
ax.add_patch(trap_box)

ax.text(-4.5, 3.5,
       'WRONG METRICS',
       ha='center',
       fontsize=9,
       fontweight='bold',
       color=WHITE,
       fontfamily='sans-serif',
       zorder=9)

wrong_metrics = [
    {'text': 'Code Lines', 'y': 2.8},
    {'text': 'Sales Volume', 'y': 2.2},
    {'text': 'Feature Count', 'y': 1.6}
]

for metric in wrong_metrics:
    # Metric item
    item = Rectangle((-6.8, metric['y'] - 0.25), 4.6, 0.5,
                    facecolor=WHITE,
                    edgecolor='none',
                    alpha=0.25,
                    zorder=9)
    ax.add_patch(item)

    ax.text(-4.5, metric['y'],
           metric['text'],
           ha='center',
           fontsize=7,
           color=WHITE,
           fontfamily='sans-serif',
           zorder=10)

# Middle Right: Right Metrics (Aligned)
aligned_box = Rectangle((1.5, 1.5), 6, 2.5,
                        facecolor=GREEN_SUCCESS,
                        edgecolor='none',
                        alpha=0.85,
                        zorder=8,
                        )
ax.add_patch(aligned_box)

ax.text(4.5, 3.5,
       'RIGHT METRICS',
       ha='center',
       fontsize=9,
       fontweight='bold',
       color=WHITE,
       fontfamily='sans-serif',
       zorder=9)

right_metrics = [
    {'text': 'Code Quality', 'y': 2.8},
    {'text': 'Profit Margin', 'y': 2.2},
    {'text': 'Feature Usage', 'y': 1.6}
]

for metric in right_metrics:
    # Metric item
    item = Rectangle((2.2, metric['y'] - 0.25), 4.6, 0.5,
                    facecolor=WHITE,
                    edgecolor='none',
                    alpha=0.25,
                    zorder=9)
    ax.add_patch(item)

    ax.text(4.5, metric['y'],
           metric['text'],
           ha='center',
           fontsize=7,
           color=WHITE,
           fontfamily='sans-serif',
           zorder=10)

# Bottom Left: Failure Result (Green metrics, failed company)
fail_result = Rectangle((-7.5, -2.5), 6, 3,
                       facecolor='#fed7d7',
                       edgecolor=RED_WARNING,
                       linewidth=2,
                       alpha=0.7,
                       zorder=7,
                       )
ax.add_patch(fail_result)

ax.text(-4.5, -0.5,
       'RESULT: FAILURE',
       ha='center',
       fontsize=8,
       fontweight='bold',
       color=RED_WARNING,
       fontfamily='sans-serif',
       zorder=8)

ax.text(-4.5, -1.0,
       '"All metrics green,',
       ha='center',
       fontsize=7,
       color=DEEP_BLUE,
       fontfamily='sans-serif',
       style='italic',
       zorder=8)

ax.text(-4.5, -1.5,
       'but company failed"',
       ha='center',
       fontsize=7,
       color=DEEP_BLUE,
       fontfamily='sans-serif',
       style='italic',
       zorder=8)

# Checkmarks showing green metrics
checkmarks = [(-6.2, -2), (-4.5, -2), (-2.8, -2)]
for x, y in checkmarks:
    ax.text(x, y,
           '✓',
           ha='center',
           fontsize=16,
           color=GREEN_SUCCESS,
           fontweight='bold',
           zorder=8)

# Bottom Right: Success Result (Aligned metrics, thriving company)
success_result = Rectangle((1.5, -2.5), 6, 3,
                          facecolor='#c6f6d5',
                          edgecolor=GREEN_SUCCESS,
                          linewidth=2,
                          alpha=0.7,
                          zorder=7,
                          )
ax.add_patch(success_result)

ax.text(4.5, -0.5,
       'RESULT: SUCCESS',
       ha='center',
       fontsize=8,
       fontweight='bold',
       color=GREEN_SUCCESS,
       fontfamily='sans-serif',
       zorder=8)

ax.text(4.5, -1.0,
       '"Metrics aligned,',
       ha='center',
       fontsize=7,
       color=DEEP_BLUE,
       fontfamily='sans-serif',
       style='italic',
       zorder=8)

ax.text(4.5, -1.5,
       'company thrives"',
       ha='center',
       fontsize=7,
       color=DEEP_BLUE,
       fontfamily='sans-serif',
           style='italic',
       zorder=8)

# Upward trend chart
trend_x = np.array([2.5, 3.5, 4.5, 5.5, 6.5])
trend_y = np.array([-2.2, -1.9, -1.6, -1.3, -1.0])
ax.plot(trend_x, trend_y,
       color=GREEN_SUCCESS,
       linewidth=2,
       marker='o',
       markersize=4,
       zorder=8)

# Connection arrows
# From strategy to wrong metrics
arrow_wrong = FancyArrowPatch((-2, 4.2), (-5, 4),
                             arrowstyle='->',
                             mutation_scale=15,
                             linewidth=2.5,
                             color=RED_WARNING,
                             alpha=0.6,
                             zorder=5,
                             connectionstyle="arc3,rad=-0.3")
ax.add_patch(arrow_wrong)

# From strategy to right metrics
arrow_right = FancyArrowPatch((2, 4.2), (5, 4),
                             arrowstyle='->',
                             mutation_scale=15,
                             linewidth=2.5,
                             color=GREEN_SUCCESS,
                             alpha=0.6,
                             zorder=5,
                             connectionstyle="arc3,rad=0.3")
ax.add_patch(arrow_right)

# From wrong metrics to failure
arrow_fail = FancyArrowPatch((-4.5, 1.5), (-4.5, 0.5),
                            arrowstyle='->',
                            mutation_scale=15,
                            linewidth=2.5,
                            color=RED_WARNING,
                            alpha=0.5,
                            zorder=5)
ax.add_patch(arrow_fail)

# From right metrics to success
arrow_success = FancyArrowPatch((4.5, 1.5), (4.5, 0.5),
                              arrowstyle='->',
                              mutation_scale=15,
                              linewidth=2.5,
                              color=GREEN_SUCCESS,
                              alpha=0.5,
                              zorder=5)
ax.add_patch(arrow_success)

# Warning symbol on wrong metrics
warning = Circle((-7.5, 3.75), 0.4,
               facecolor=RED_WARNING,
               edgecolor=WHITE,
               linewidth=2,
               alpha=0.9,
               zorder=11)
ax.add_patch(warning)

ax.text(-7.5, 3.75,
       '!',
       ha='center',
       va='center',
       fontsize=14,
       fontweight='bold',
       color=WHITE,
       zorder=12)

# Checkmark on right metrics
check = Circle((7.5, 3.75), 0.4,
              facecolor=GREEN_SUCCESS,
              edgecolor=WHITE,
              linewidth=2,
              alpha=0.9,
              zorder=11)
ax.add_patch(check)

ax.text(7.5, 3.75,
       '✓',
       ha='center',
       va='center',
       fontsize=12,
       fontweight='bold',
       color=WHITE,
       zorder=12)

# Bottom text
fig.text(0.5, 0.08,
         'THE KPI TRAP',
         ha='center',
         fontsize=14,
         fontweight='semibold',
         color=DEEP_BLUE,
         alpha=0.8,
         fontfamily='sans-serif')

fig.text(0.5, 0.04,
         'when metrics misalign with strategy · employees vote with their behavior',
         ha='center',
         fontsize=7,
         fontweight='light',
         color=NEUTRAL_GRAY,
         alpha=0.6,
         fontfamily='sans-serif')

plt.tight_layout(pad=0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save
output_path = 'kpi_trap_concept.png'
plt.savefig(output_path,
           dpi=300,
           facecolor='#fafafa',
           edgecolor='none',
           bbox_inches='tight',
           pad_inches=0.2)

print(f"Design created: {output_path}")
plt.close()
