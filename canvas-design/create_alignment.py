import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Wedge
from matplotlib import font_manager
import os

# Set up the figure with high DPI for quality
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

# Background - subtle off-white for warmth
ax.set_facecolor('#fafafa')
fig.patch.set_facecolor('#fafafa')

# Create the central target (the unified objective)
central_circle = Circle((0, 0), 1.2, color=DEEP_BLUE, zorder=10, alpha=0.95)
ax.add_patch(central_circle)

# Inner ring - suggesting focus
inner_ring = Circle((0, 0), 0.7, color=WHITE, zorder=11, alpha=0.3)
ax.add_patch(inner_ring)

# Core - the essence of alignment
core = Circle((0, 0), 0.35, color=RADIANT_ORANGE, zorder=12, alpha=1.0)
ax.add_patch(core)

# Create convergent arrows from multiple directions
# Each arrow represents a team or individual aligning to the central goal

num_arrows = 12
arrow_length = 5.5
arrow_start_radius = 7

for i in range(num_arrows):
    angle = 2 * np.pi * i / num_arrows

    # Starting point (periphery)
    start_x = arrow_start_radius * np.cos(angle)
    start_y = arrow_start_radius * np.sin(angle)

    # Ending point (at central circle edge)
    end_x = 1.3 * np.cos(angle)
    end_y = 1.3 * np.sin(angle)

    # Create tapered arrow path (not just a line, but a shape)
    # Arrow width varies along length
    width_start = 0.18
    width_end = 0.35

    # Create the arrow shape manually for more control
    # Direction vector
    dx = end_x - start_x
    dy = end_y - start_y
    length = np.sqrt(dx**2 + dy**2)
    ux, uy = dx/length, dy/length  # unit vector
    px, py = -uy, ux  # perpendicular vector

    # Arrow points
    p1 = (start_x + width_start * px, start_y + width_start * py)
    p2 = (start_x - width_start * px, start_y - width_start * py)
    p3 = (end_x - width_end * px, end_y - width_end * py)
    p4 = (end_x + width_end * px, end_y + width_end * py)

    # Arrowhead points
    arrowhead_length = 0.8
    arrowhead_width = 0.7

    tip = (end_x, end_y)
    base1 = (end_x - arrowhead_length * ux + arrowhead_width * px,
             end_y - arrowhead_length * uy + arrowhead_width * py)
    base2 = (end_x - arrowhead_length * ux - arrowhead_width * px,
             end_y - arrowhead_length * uy - arrowhead_width * py)

    # Draw arrow shaft (gradient effect using alpha)
    shaft = patches.Polygon([p1, p2, p3, p4],
                           closed=True,
                           facecolor=NEUTRAL_GRAY,
                           edgecolor='none',
                           alpha=0.6,
                           zorder=5)
    ax.add_patch(shaft)

    # Draw arrowhead
    arrowhead = patches.Polygon([tip, base1, base2],
                               closed=True,
                               facecolor=RADIANT_ORANGE,
                               edgecolor='none',
                               alpha=0.9,
                               zorder=6)
    ax.add_patch(arrowhead)

# Add subtle orbital rings to suggest dynamic movement
for radius in [2.5, 4.0, 5.5]:
    circle = Circle((0, 0), radius,
                   fill=False,
                   edgecolor=LIGHT_GRAY,
                   linewidth=0.8,
                   linestyle='--',
                   alpha=0.4,
                   zorder=3)
    ax.add_patch(circle)

# Add small indicator dots on arrows (team markers)
for i in range(num_arrows):
    angle = 2 * np.pi * i / num_arrows
    dot_x = 5.5 * np.cos(angle)
    dot_y = 5.5 * np.sin(angle)

    dot = Circle((dot_x, dot_y), 0.18,
                color=DEEP_BLUE,
                alpha=0.8,
                zorder=7)
    ax.add_patch(dot)

# Add subtle text at bottom (minimal, typographic)
# Try to use a nice font, fall back to sans-serif if not available
fig.text(0.5, 0.08,
         'ALIGNMENT',
         ha='center',
         fontsize=14,
         fontweight='light',
         color=DEEP_BLUE,
         alpha=0.7,
         fontfamily='sans-serif',
         style='italic')

fig.text(0.5, 0.04,
         'convergence · unity · purpose',
         ha='center',
         fontsize=8,
         fontweight='light',
         color=NEUTRAL_GRAY,
         alpha=0.6,
         fontfamily='sans-serif')

# Tight layout
plt.tight_layout(pad=0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save as high-quality PNG
output_path = 'goal_alignment.png'
plt.savefig(output_path,
           dpi=300,
           facecolor='#fafafa',
           edgecolor='none',
           bbox_inches='tight',
           pad_inches=0.2)

print(f"Design saved to: {output_path}")
print(f"Philosophy: Radiant Convergence")
print(f"Concept: Team Goal Alignment")
print(f"Format: 16:9 (300 DPI)")
