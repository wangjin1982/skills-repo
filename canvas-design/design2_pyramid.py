import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch
from matplotlib import font_manager

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
TEAL = '#319795'

# Background
ax.set_facecolor('#fafafa')
fig.patch.set_facecolor('#fafafa')

# Style 2: Pyramid Alignment - Hierarchical design
# Create a pyramid structure representing different levels aligning to top

# Pyramid levels
levels = [
    {'y': -4, 'width': 16, 'color': '#e2e8f0', 'label': 'TEAMS', 'count': 8},
    {'y': -2.2, 'width': 11, 'color': '#cbd5e0', 'label': 'MANAGERS', 'count': 5},
    {'y': -0.4, 'width': 6, 'color': '#a0aec0', 'label': 'LEADERS', 'count': 3},
    {'y': 1.4, 'width': 2.5, 'color': DEEP_BLUE, 'label': 'GOAL', 'count': 1}
]

# Draw pyramid levels with connection lines
for i, level in enumerate(levels):
    y = level['y']
    width = level['width']
    color = level['color']
    label = level['label']

    # Draw level bar
    if i == len(levels) - 1:  # Top level (goal)
        # Draw target circle
        target = Circle((0, y + 0.4), 1.2, color=DEEP_BLUE, alpha=0.95, zorder=10)
        ax.add_patch(target)

        # Inner glow
        inner = Circle((0, y + 0.4), 0.5, color=RADIANT_ORANGE, alpha=1.0, zorder=11)
        ax.add_patch(inner)

        # Label
        ax.text(0, y + 0.4, label,
               ha='center',
               va='center',
               fontsize=9,
               fontweight='bold',
               color=WHITE,
               fontfamily='sans-serif',
               zorder=12)
    else:
        # Draw rectangular level
        rect = Rectangle((-width/2, y), width, 0.8,
                        facecolor=color,
                        edgecolor='none',
                        alpha=0.7,
                        zorder=5)
        ax.add_patch(rect)

        # Draw nodes (teams/managers) on this level
        count = level['count']
        if count > 1:
            spacing = width / (count + 1)
            for j in range(count):
                x_pos = -width/2 + spacing * (j + 1)
                node = Circle((x_pos, y + 0.4), 0.35, color=DEEP_BLUE, alpha=0.8, zorder=6)
                ax.add_patch(node)
        else:
            # Single node
            node = Circle((0, y + 0.4), 0.35, color=DEEP_BLUE, alpha=0.8, zorder=6)
            ax.add_patch(node)

# Draw convergent arrows from each level to the level above
for i in range(len(levels) - 1):
    current_level = levels[i]
    next_level = levels[i + 1]

    current_y = current_level['y'] + 0.8
    next_y = next_level['y']
    current_width = current_level['width']
    next_width = next_level['width']
    current_count = current_level['count']

    if current_count > 1:
        spacing = current_width / (current_count + 1)
        for j in range(current_count):
            x_start = -current_width/2 + spacing * (j + 1)
            # Calculate target x on next level
            next_count = next_level['count']
            if next_count > 1:
                next_spacing = next_width / (next_level['count'] + 1)
                # Target to nearest parent node
                target_idx = min(j, next_level['count'] - 1)
                x_end = -next_width/2 + next_spacing * (target_idx + 1)
            else:
                x_end = 0

            # Draw arrow
            arrow = FancyArrowPatch((x_start, current_y), (x_end, next_y),
                                  arrowstyle='->',
                                  mutation_scale=15,
                                  linewidth=1.2,
                                  color=NEUTRAL_GRAY,
                                  alpha=0.4,
                                  zorder=4)
            ax.add_patch(arrow)

# Add vertical guide lines on sides
ax.plot([-8, -2.5], [-3.6, 1.8], color=LIGHT_GRAY, linewidth=1.5, alpha=0.3, zorder=2)
ax.plot([8, 2.5], [-3.6, 1.8], color=LIGHT_GRAY, linewidth=1.5, alpha=0.3, zorder=2)

# Add level labels on the right
for i, level in enumerate(levels):
    if i < len(levels) - 1:  # Skip top level
        ax.text(9, level['y'] + 0.4,
               level['label'],
               ha='left',
               va='center',
               fontsize=8,
               fontweight='light',
               color=NEUTRAL_GRAY,
               fontfamily='sans-serif')

# Add subtle text at bottom
fig.text(0.5, 0.08,
         'HIERARCHICAL ALIGNMENT',
         ha='center',
         fontsize=16,
         fontweight='semibold',
         color=DEEP_BLUE,
         alpha=0.8,
         fontfamily='sans-serif')

fig.text(0.5, 0.04,
         'structure · clarity · execution',
         ha='center',
         fontsize=7,
         fontweight='light',
         color=NEUTRAL_GRAY,
         alpha=0.6,
         fontfamily='sans-serif')

plt.tight_layout(pad=0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save
output_path = 'goal_alignment_style2.png'
plt.savefig(output_path,
           dpi=300,
           facecolor='#fafafa',
           edgecolor='none',
           bbox_inches='tight',
           pad_inches=0.2)

print(f"Style 2 created: {output_path}")
plt.close()
