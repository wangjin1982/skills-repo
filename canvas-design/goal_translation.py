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
PURPLE = '#805ad5'
TEAL = '#319795'

# Background
ax.set_facecolor('#fafafa')
fig.patch.set_facecolor('#fafafa')

# Concept: Goal Translation - breaking down company goal into functional goals

# Top: Company Goal
company_box = Rectangle((-4, 4.5), 8, 1.5,
                       facecolor=DEEP_BLUE,
                       edgecolor='none',
                       alpha=0.9,
                       zorder=10,
                       )
ax.add_patch(company_box)

ax.text(0, 5.25,
       'COMPANY GOAL',
       ha='center',
       fontsize=10,
       fontweight='bold',
       color=WHITE,
       fontfamily='sans-serif',
       zorder=11)

ax.text(0, 4.75,
       'Revenue Growth 30%',
       ha='center',
       fontsize=8,
       color=WHITE,
       fontfamily='sans-serif',
       zorder=11)

# Middle: Translation Layer (The Manager)
translation_circle = Circle((0, 2), 1.3,
                           facecolor=RADIANT_ORANGE,
                           edgecolor=WHITE,
                           linewidth=3,
                           alpha=0.95,
                           zorder=12)
ax.add_patch(translation_circle)

ax.text(0, 2.15,
       'GOAL',
       ha='center',
       fontsize=9,
       fontweight='bold',
       color=WHITE,
       fontfamily='sans-serif',
       zorder=13)

ax.text(0, 1.75,
       'TRANSLATION',
       ha='center',
       fontsize=7,
       color=WHITE,
       fontfamily='sans-serif',
       zorder=13)

# Bottom: Functional Goals (4 roles)
roles = [
    {'x': -6, 'color': PURPLE, 'title': 'PRODUCT', 'metric': 'User Retention\n20% → 30%'},
    {'x': -2, 'color': TEAL, 'title': 'R&D', 'metric': 'System Uptime\n99.5% → 99.9%'},
    {'x': 2, 'color': '#e53e3e', 'title': 'SALES', 'metric': 'Deal Cycle\n30 → 20 days'},
    {'x': 6, 'color': '#d69e2e', 'title': 'CS', 'metric': 'Renewal Rate\n80% → 90%'}
]

for role in roles:
    # Role box
    role_box = Rectangle((role['x'] - 1.3, -3), 2.6, 1.5,
                        facecolor=role['color'],
                        edgecolor='none',
                        alpha=0.85,
                        zorder=10,
                        )
    ax.add_patch(role_box)

    # Role title
    ax.text(role['x'], -2.3,
           role['title'],
           ha='center',
           fontsize=8,
           fontweight='bold',
           color=WHITE,
           fontfamily='sans-serif',
           zorder=11)

    # Role metric
    ax.text(role['x'], -2.85,
           role['metric'],
           ha='center',
           fontsize=7,
           color=WHITE,
           fontfamily='sans-serif',
           zorder=11)

# Arrows from company to translation
for angle in [225, 270, 315]:
    rad = np.deg2rad(angle)
    start_x = 2.5 * np.cos(rad)
    start_y = 4.5 + 1.5 * np.sin(rad)
    end_x = 1.3 * np.cos(rad)
    end_y = 2 + 1.3 * np.sin(rad)

    arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y),
                           arrowstyle='->',
                           mutation_scale=12,
                           linewidth=2,
                           color=DEEP_BLUE,
                           alpha=0.5,
                           zorder=5)
    ax.add_patch(arrow)

# Arrows from translation to roles
for i, role in enumerate(roles):
    start_x = 0
    start_y = 0.7
    end_x = role['x']
    end_y = -1.5

    arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y),
                           arrowstyle='->',
                           mutation_scale=12,
                           linewidth=2,
                           color=RADIANT_ORANGE,
                           alpha=0.5,
                           zorder=5,
                           connectionstyle=f"arc3,rad={0.3 if i < 2 else -0.3}")
    ax.add_patch(arrow)

# Side annotations
# Left: Without Translation (Chaos)
ax.text(-8.5, 0,
       'WITHOUT\nTRANSLATION',
       ha='center',
       fontsize=7,
       fontweight='bold',
       color='#e53e3e',
       fontfamily='sans-serif',
       style='italic',
       zorder=6)

# Chaotic arrows
chaotic_arrows = [(-9.5, 3, -7.5, 2), (-9.5, 0, -7.5, -1), (-9.5, -3, -7.5, -2)]
for start_x, start_y, end_x, end_y in chaotic_arrows:
    arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y),
                           arrowstyle='->',
                           mutation_scale=10,
                           linewidth=1.5,
                           color='#e53e3e',
                           alpha=0.4,
                           zorder=4)
    ax.add_patch(arrow)

# Right: With Translation (Alignment)
ax.text(8.5, 0,
       'WITH\nTRANSLATION',
       ha='center',
       fontsize=7,
       fontweight='bold',
       color='#38a169',
       fontfamily='sans-serif',
       style='italic',
       zorder=6)

# Aligned arrows
aligned_start = (7.5, 2)
aligned_ends = [(9, 1), (9, 0), (9, -1), (9, -2)]
for end_x, end_y in aligned_ends:
    arrow = FancyArrowPatch((aligned_start[0], aligned_start[1]), (end_x, end_y),
                           arrowstyle='->',
                           mutation_scale=10,
                           linewidth=1.5,
                           color='#38a169',
                           alpha=0.4,
                           zorder=4)
    ax.add_patch(arrow)

# Bottom text
fig.text(0.5, 0.08,
         'GOAL TRANSLATION',
         ha='center',
         fontsize=14,
         fontweight='semibold',
         color=DEEP_BLUE,
         alpha=0.8,
         fontfamily='sans-serif')

fig.text(0.5, 0.04,
         'from company vision to functional metrics · the manager as translator',
         ha='center',
         fontsize=7,
         fontweight='light',
         color=NEUTRAL_GRAY,
         alpha=0.6,
         fontfamily='sans-serif')

plt.tight_layout(pad=0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save
output_path = 'goal_translation_concept.png'
plt.savefig(output_path,
           dpi=300,
           facecolor='#fafafa',
           edgecolor='none',
           bbox_inches='tight',
           pad_inches=0.2)

print(f"Design created: {output_path}")
plt.close()
