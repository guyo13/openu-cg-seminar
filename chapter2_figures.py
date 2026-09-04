import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Circle
import math

def lens_geometry():

    # Constants
    d = 1.0
    u_x, u_y = -d/2, 0
    v_x, v_y = d/2, 0
    p_x, p_y = 0, math.sqrt(d**2 - (d/2)**2)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the two circles with radius d
    circle_u = Circle((u_x, u_y), d, color='blue', fill=False, linestyle='--', alpha=0.4)
    circle_v = Circle((v_x, v_y), d, color='red', fill=False, linestyle='--', alpha=0.4)
    ax.add_patch(circle_u)
    ax.add_patch(circle_v)

    # Generate points for the top lens (Blue area)
    # Angles for arc centered at u (from v to P)
    angles_u_top = np.linspace(0, np.pi/3, 100)
    arc_u_x_top = u_x + d * np.cos(angles_u_top)
    arc_u_y_top = u_y + d * np.sin(angles_u_top)

    # Angles for arc centered at v (from P to u)
    angles_v_top = np.linspace(2*np.pi/3, np.pi, 100)
    arc_v_x_top = v_x + d * np.cos(angles_v_top)
    arc_v_y_top = v_y + d * np.sin(angles_v_top)

    top_lens_x = np.concatenate([arc_u_x_top, arc_v_x_top])
    top_lens_y = np.concatenate([arc_u_y_top, arc_v_y_top])
    ax.fill(top_lens_x, top_lens_y, color='skyblue', alpha=0.5, label='Top Half (Clique 1)')

    # Generate points for the bottom lens (Red area)
    angles_u_bottom = np.linspace(0, -np.pi/3, 100)
    arc_u_x_bottom = u_x + d * np.cos(angles_u_bottom)
    arc_u_y_bottom = u_y + d * np.sin(angles_u_bottom)

    angles_v_bottom = np.linspace(-2*np.pi/3, -np.pi, 100)
    arc_v_x_bottom = v_x + d * np.cos(angles_v_bottom)
    arc_v_y_bottom = v_y + d * np.sin(angles_v_bottom)

    bottom_lens_x = np.concatenate([arc_u_x_bottom, arc_v_x_bottom])
    bottom_lens_y = np.concatenate([arc_u_y_bottom, arc_v_y_bottom])
    ax.fill(bottom_lens_x, bottom_lens_y, color='lightcoral', alpha=0.5, label='Bottom Half (Clique 2)')

    # Draw Equilateral Triangle
    triangle = Polygon([[u_x, u_y], [v_x, v_y], [p_x, p_y]], closed=True, fill=False, edgecolor='black', linewidth=2.5, zorder=5)
    ax.add_patch(triangle)

    # Draw dividing line
    ax.plot([-1.2, 1.2], [0, 0], color='black', linestyle='-.', zorder=4, alpha=0.7)

    # Plot points u, v, P
    ax.scatter([u_x, v_x, p_x], [u_y, v_y, p_y], color='black', zorder=6, s=80)

    # Annotations
    ax.text(u_x - 0.12, u_y - 0.1, 'u', fontsize=16, fontweight='bold')
    ax.text(v_x + 0.12, v_y - 0.1, 'v', fontsize=16, fontweight='bold')
    ax.text(p_x, p_y + 0.08, 'P', fontsize=16, fontweight='bold', ha='center')

    # Distance labels for the triangle edges
    ax.text(0, -0.08, 'd', fontsize=14, ha='center', va='top', fontweight='bold')
    ax.text(-0.35, 0.45, 'd', fontsize=14, ha='right', fontweight='bold')
    ax.text(0.35, 0.45, 'd', fontsize=14, ha='left', fontweight='bold')

    # Setup plot limits and display
    ax.set_aspect('equal')
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.2, 1.6)
    ax.axis('off')
    plt.legend(loc='upper right', fontsize=12)
    plt.title('The Co-Bipartite Lens Region', fontsize=16, fontweight='bold')

    plt.tight_layout()
    return fig

def slab_geom():
    # Coordinates for points a and b
    a_x, a_y = 1, 2
    b_x, b_y = 6, 4

    y_max = 7
    y_min = 0

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the line segment ab
    ax.plot([a_x, b_x], [a_y, b_y], color='black', linewidth=2.5, zorder=4)
    ax.scatter([a_x, b_x], [a_y, b_y], color='black', s=80, zorder=5)

    # Plot the vertical bounding lines l_a^v and l_b^v
    ax.axvline(x=a_x, color='gray', linestyle='--', linewidth=1.5, zorder=2)
    ax.axvline(x=b_x, color='gray', linestyle='--', linewidth=1.5, zorder=2)

    # Fill the Upper Slab U_ab
    ax.fill_between([a_x, b_x], [a_y, b_y], y_max, color='skyblue', alpha=0.5, label='Upper Slab ($U_{ab}$)', zorder=1)

    # Fill the Lower Slab \overline{U}_ab
    ax.fill_between([a_x, b_x], y_min, [a_y, b_y], color='lightcoral', alpha=0.5, label='Lower Slab ($\\overline{U}_{ab}$)', zorder=1)

    # Annotations
    ax.text(a_x - 0.2, a_y, 'a', fontsize=16, fontweight='bold', ha='right')
    ax.text(b_x + 0.2, b_y, 'b', fontsize=16, fontweight='bold', ha='left')
    ax.text(a_x, y_max - 0.5, ' $l_a^v$', fontsize=14, color='gray')
    ax.text(b_x, y_max - 0.5, ' $l_b^v$', fontsize=14, color='gray')
    ax.text((a_x + b_x)/2, (a_y + b_y)/2 + 1.5, '$U_{ab}$ (Upper Slab)', fontsize=14, fontweight='bold', ha='center')
    ax.text((a_x + b_x)/2, (a_y + b_y)/2 - 1.5, '$\\overline{U}_{ab}$ (Lower Slab)', fontsize=14, fontweight='bold', ha='center')

    # Setup plot limits and display
    ax.set_xlim(a_x - 2, b_x + 2)
    ax.set_ylim(y_min, y_max)
    ax.axis('off')
    ax.legend(loc='upper left', fontsize=12)
    plt.title('The Slab-Based Regions', fontsize=16, fontweight='bold')

    plt.tight_layout()
    return fig
