from solid import *  # Import solidpython functions
from solid.utils import *  # Utilities for transformations

# Parameters for the glass
outer_radius = 60  # Outer radius of the glass in mm
height = 120  # Height of the glass in mm
wall_thickness = 2  # Thickness of the glass walls in mm

print(f"Params: {outer_radius=} {height=} {wall_thickness=}")

# Outer cylinder representing the glass body
outer_cylinder = cylinder(r=outer_radius, h=height)

# Inner cylinder to hollow out the glass
inner_radius = outer_radius - wall_thickness
inner_cylinder = cylinder(r=inner_radius, h=height)

# Subtract the inner cylinder from the outer to create the hollow
glass = outer_cylinder - up(0.5)(inner_cylinder)

# Export the design to a .scad file
scad_render_to_file(glass, 'drinking_glass.scad')
