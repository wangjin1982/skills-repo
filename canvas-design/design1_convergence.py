import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle
import matplotlib.patheffects as path_effects

# Set up the figure with high DPI
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=300)
ax.set_xlim(-10, 10)
ax.set_ylim(-6, 6)
ax.set_aspect('equal')
ax.axis('off')

# Color palette - professional business style
DEEP_BLUE = '#1a365d'
RADIANT_ORANGE = '#ed8936'
NEUTRAL_GRAY = '#718096'
LIGHT_GRAY = '#e2e8f0'
WHITE = '#ffffff'
GOLD = '#d69e2e'

# Background
ax.set_facecolor('#fafafa')
fig.patch.set_facecolor('#fafafa')

# Style 1: Radiant Convergence - Classic arrow design
# Central target with glow effect
for radius in [1.5, 1.4, 1.3, 1.2]:
    alpha = 0.1 + (1.5 - radius) * 0.2
    circle = Circle((0, 0), radius, color=RADIANT_ORANGE, alpha=alpha, zorder=8)
    ax.add_patch(circle)

central_circle = Circle((0, 0), 1.0, color=DEEP_BLUE, zorder=10, alpha=0.95)
ax.add_patch(central_circle)

core = Circle((0, 0), 0.3, color=RADIANT_ORANGE, zorder=12, alpha=1.0)
ax.add_patch(core)

# Create convergent arrows
num_arrows = 16
arrow_length = 6
arrow_start_radius = 7.5

for i in range(num_arrows):
    angle = 2 * np.pi * i / num_arrows

    # Starting point
    start_x = arrow_start_radius * np.cos(angle)
    start_y = arrow_start_radius * np.sin(angle)

    # Ending point
    end_x = 1.2 * np.cos(angle)
    end_y = 1.2 * np.sin(angle)

    # Direction vectors
    dx = end_x - start_x
    dy = end_y - start_y
    length = np.sqrt(dx**2 + dy**2)
    ux, uy = dx/length, dy/length
    px, py = -uy, ux

    # Arrow dimensions
    width_start = 0.12
    width_end = 0.28

    p1 = (start_x + width_start * px, start_y + width_start * py)
    p2 = (start_x - width_start * px, start_y - width_start * py)
    p3 = (end_x - width_end * px, end_y - width_end * py)
    p4 = (end_x + width_end * px, end_y + width_end * py)

    # Draw shaft
    shaft = patches.Polygon([p1, p2, p3, p4],
                           closed=True,
                           facecolor=NEUTRAL_GRAY,
                           edgecolor='none',
                           alpha=0.5,
                           zorder=5)
    ax.add_patch(shaft)

    # Arrowhead
    arrowhead_length = 0.7
    arrowhead_width = 0.55

    tip = (end_x, end_y)
    base1 = (end_x - arrowhead_length * ux + arrowhead_width * px,
             end_y - arrowhead_length * uy + arrowhead_width * py)
    base2 = (end_x - arrowhead_length * ux - arrowhead_width * px,
             end_y - arrowhead_length * uy - arrowhead_width * py)

    arrowhead = patches.Polygon([tip, base1, base2],
                               closed=True,
                               facecolor=RADIANT_ORANGE,
                               edgecolor='none',
                               alpha=0.95,
                               zorder=6)
    ax.add_patch(arrowhead)

    # Team marker dots
    dot_x = 6.5 * np.cos(angle)
    dot_y = 6.5 * np.sin(angle)
    dot = Circle((dot_x, dot_y), 0.15,
                color=DEEP_BLUE,
                alpha=0.85,
                zorder=7)
    ax.add_patch(dot)

# Add orbital rings
for radius in [2.2, 3.8, 5.4]:
    circle = Circle((0, 0), radius,
                   fill=False,
                   edgecolor=LIGHT_GRAY,
                   linewidth=0.6,
                   linestyle=':',
                   alpha=0.35,
                   zorder=3)
    ax.add_patch(circle)

# Add subtle text
fig.text(0.5, 0.08,
         'GOAL ALIGNMENT',
         ha='center',
         fontsize=16,
         fontweight='semibold',
         color=DEEP_BLUE,
         alpha=0.8,
         fontfamily='sans-serif')

fig.text(0.5, 0.04,
         'convergence · focus · results',
         ha='center',
         fontsize=7,
         fontweight='light',
         color=NEUTRAL_GRAY,
         alpha=0.6,
         fontfamily='sans-serif')

plt.tight_layout(pad=0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save
output_path = 'goal_alignment_style1.png'
plt.savefig(output_path,
           dpi=300,
           facecolor='#fafafa',
           edgecolor='none',
           bbox_inches='tight',
           pad_inches=0.2)

print(f"Style 1 created: {output_path}")
plt.close()
