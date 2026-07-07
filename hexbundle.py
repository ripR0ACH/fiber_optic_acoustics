import numpy as np
import jax.numpy as jnp
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

class HexagonalBundle:
    def __init__(self, R_max, r_core, r_clad):
        """
        R_max: Radius of the main circular enclosure boundary.
        r_hex: Outer radius of an individual hexagon (center to vertex distance).
        """
        self.R_max = R_max
        self.r_hex = r_core + r_clad
        self.r_core = r_core
        self.r_clad = r_clad
        self.centers = self.generate_packed_centers()

    def generate_packed_centers(self):
        # The inner radius (center to flat edge) is r_hex * sqrt(3)/2
        # Vertical row spacing between adjacent centers is 2 * inner_radius
        row_spacing = self.r_hex * np.sqrt(3)
        
        # Estimate the number of steps required to clear the boundaries
        max_rings = int(np.ceil(self.R_max / (self.r_hex * 0.75))) + 1
        
        centers = []
        
        # Loop through axial coordinate dimensions (-N to N)
        for q in range(-max_rings, max_rings + 1):
            for r in range(-max_rings, max_rings + 1):
                # FIXED MATH FOR FLAT-TOPPED HEXAGONS:
                # Horizontal step is 1.5 * radius per column index
                x_c = self.r_hex * (3.0 / 2.0 * q)
                # Vertical step accounts for the row index + half-step offset per column
                y_c = self.r_hex * (np.sqrt(3.0) * r + np.sqrt(3.0) / 2.0 * q)
                
                # Check distance from the bundle origin center
                center_dist = np.sqrt(x_c**2 + y_c**2)
                
                # Filter: Keep if the entire hexagon fits inside the outer boundary wall
                if center_dist + self.r_hex <= self.R_max:
                    centers.append([x_c, y_c])
                    
        return jnp.array(centers)

    def plot(self, figsize=(8, 8)):
        fig, ax = plt.subplots(figsize=figsize)
        
        # Draw the target perimeter circular boundary
        boundary_circle = plt.Circle((0, 0), self.R_max, color='r', fill=False, linestyle='--', linewidth=2, label="Boundary")
        ax.add_patch(boundary_circle)
        
        # Draw each packed hexagon cleanly
        # orientation=0 matches flat-topped geometry
        for center in self.centers:
            hex_patch = RegularPolygon(
                (center[0], center[1]), 
                numVertices=6, 
                radius=self.r_hex, 
                orientation=np.pi / 6, 
                facecolor='lightgray', 
                edgecolor='black', 
                linewidth=1.2,
                alpha=0.7
            )
            ax.add_patch(hex_patch)
            hex_patch = RegularPolygon(
                (center[0], center[1]), 
                numVertices=6, 
                radius=self.r_core, 
                orientation=np.pi / 6, 
                facecolor='red', 
                edgecolor='black', 
                linewidth=1.2,
                alpha=0.7
            )
            ax.add_patch(hex_patch)
            
        # Clean up axes formatting
        padding = self.r_hex * 2
        ax.set_xlim(-self.R_max - padding, self.R_max + padding)
        ax.set_ylim(-self.R_max - padding, self.R_max + padding)
        ax.set_aspect('equal')
        ax.grid(True, linestyle=':', alpha=0.3)
        plt.title(f"Perfect Honeycomb Packing (Total Hexagons: {len(self.centers)})")
        
        return fig, ax

if __name__ == "__main__":
    # Fill a 10mm bundle core with 1mm radius hexagons
    bundle = HexagonalBundle(R_max=2e-3, r_core = 220e-6, r_clad = 20e-6)
    fig, ax = bundle.plot()
    plt.show()