import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
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

# Title concept: Management Evolution - Old vs New

# Split the design into two halves: Left (Old) and Right (New)

# Divider line
ax.axvline(x=0, color=LIGHT_GRAY, linewidth=2, linestyle='-', alpha=0.5, zorder=1)

# === LEFT SIDE: Traditional Management ===

# Title
ax.text(-5, 5, 'TRADITIONAL',
       ha='center',
       fontsize=11,
       fontweight='bold',
       color=RED_WARNING,
       fontfamily='sans-serif',
       style='italic')

ax.text(-5, 4.3, 'Command - Check - Punish',
       ha='center',
       fontsize=7,
       color=NEUTRAL_GRAY,
       fontfamily='sans-serif')

# Three steps in a downward flow
steps_old = [
    {'y': 2.5, 'text': 'COMMAND', 'icon': '▼'},
    {'y': 0, 'text': 'CHECK', 'icon': '⬠'},
    {'y': -2.5, 'text': 'PUNISH', 'icon': '✕'}
]

for step in steps_old:
    # Circle background
    circle = Circle((-5, step['y']), 0.9,
                   facecolor=WHITE,
                   edgecolor=RED_WARNING,
                   linewidth=2,
                   alpha=0.8,
                   zorder=5)
    ax.add_patch(circle)

    # Text
    ax.text(-5, step['y'] + 0.25,
           step['text'],
           ha='center',
           fontsize=8,
           fontweight='bold',
           color=DEEP_BLUE,
           fontfamily='sans-serif',
           zorder=6)

    # Icon
    ax.text(-5, step['y'] - 0.35,
           step['icon'],
           ha='center',
           fontsize=14,
           color=RED_WARNING,
           zorder=6)

# Arrows connecting steps (downward)
for i in range(len(steps_old) - 1):
    arrow = FancyArrowPatch((-5, steps_old[i]['y'] - 0.95),
                           (-5, steps_old[i+1]['y'] + 0.95),
                           arrowstyle='->',
                           mutation_scale=15,
                           linewidth=2,
                           color=RED_WARNING,
                           alpha=0.5,
                           zorder=4)
    ax.add_patch(arrow)

# Result: Disengagement
result_box = Rectangle((-7.5, -4.5), 5, 1.2,
                      facecolor='#fed7d7',
                      edgecolor=RED_WARNING,
                      linewidth=1.5,
                      alpha=0.6,
                      zorder=3)
ax.add_patch(result_box)

ax.text(-5, -3.9,
       'Result: Disengagement',
       ha='center',
       fontsize=7,
       fontweight='bold',
       color=RED_WARNING,
       fontfamily='sans-serif',
       zorder=4)

ax.text(-5, -4.4,
       '"Just doing the minimum"',
       ha='center',
       fontsize=6,
       color=DEEP_BLUE,
       fontfamily='sans-serif',
       style='italic',
       zorder=4)

# === RIGHT SIDE: New Management ===

# Title
ax.text(5, 5, 'MODERN',
       ha='center',
       fontsize=11,
       fontweight='bold',
       color=GREEN_SUCCESS,
       fontfamily='sans-serif',
       style='italic')

ax.text(5, 4.3, 'Respect - Feedback - Growth',
       ha='center',
       fontsize=7,
       color=NEUTRAL_GRAY,
       fontfamily='sans-serif')

# Three steps in a circular/upward flow
steps_new = [
    {'y': 2.5, 'text': 'RESPECT', 'icon': '★'},
    {'y': 0, 'text': 'FEEDBACK', 'icon': '◉'},
    {'y': -2.5, 'text': 'GROWTH', 'icon': '▲'}
]

for step in steps_new:
    # Circle background
    circle = Circle((5, step['y']), 0.9,
                   facecolor=WHITE,
                   edgecolor=GREEN_SUCCESS,
                   linewidth=2,
                   alpha=0.8,
                   zorder=5)
    ax.add_patch(circle)

    # Text
    ax.text(5, step['y'] + 0.25,
           step['text'],
           ha='center',
           fontsize=8,
           fontweight='bold',
           color=DEEP_BLUE,
           fontfamily='sans-serif',
           zorder=6)

    # Icon
    ax.text(5, step['y'] - 0.35,
           step['icon'],
           ha='center',
           fontsize=14,
           color=GREEN_SUCCESS,
           zorder=6)

# Circular arrows showing continuous improvement
# Top arrow (from bottom to top)
arc_top = FancyArrowPatch((5, -1.5), (5, 1.5),
                          arrowstyle='->',
                          mutation_scale=12,
                          linewidth=1.5,
                          color=GREEN_SUCCESS,
                          alpha=0.4,
                          connectionstyle="arc3,rad=.3",
                          zorder=4)
ax.add_patch(arc_top)

# Result: Engagement
result_box_new = Rectangle((2.5, -4.5), 5, 1.2,
                          facecolor='#c6f6d5',
                          edgecolor=GREEN_SUCCESS,
                          linewidth=1.5,
                          alpha=0.6,
                          zorder=3)
ax.add_patch(result_box_new)

ax.text(5, -3.9,
       'Result: Engagement',
       ha='center',
       fontsize=7,
       fontweight='bold',
       color=GREEN_SUCCESS,
       fontfamily='sans-serif',
       zorder=4)

ax.text(5, -4.4,
       '"Fully committed"',
       ha='center',
       fontsize=6,
       color=DEEP_BLUE,
       fontfamily='sans-serif',
       style='italic',
       zorder=4)

# Central transformation arrow
big_arrow = FancyArrowPatch((-1.5, 0), (1.5, 0),
                          arrowstyle='->,head_width=0.5,head_length=0.5',
                          mutation_scale=25,
                          linewidth=4,
                          color=RADIANT_ORANGE,
                          alpha=0.7,
                          zorder=2)
ax.add_patch(big_arrow)

# Bottom text
fig.text(0.5, 0.08,
         'MANAGEMENT EVOLUTION',
         ha='center',
         fontsize=14,
         fontweight='semibold',
         color=DEEP_BLUE,
         alpha=0.8,
         fontfamily='sans-serif')

fig.text(0.5, 0.04,
         'from control to empowerment · Gen Z & Millennials',
         ha='center',
         fontsize=7,
         fontweight='light',
         color=NEUTRAL_GRAY,
         alpha=0.6,
         fontfamily='sans-serif')

plt.tight_layout(pad=0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save
output_path = 'genz_management_evolution.png'
plt.savefig(output_path,
           dpi=300,
           facecolor='#fafafa',
           edgecolor='none',
           bbox_inches='tight',
           pad_inches=0.2)

print(f"Design created: {output_path}")
plt.close()
