from solid import *
from solid.utils import *

width = 100
depth = 100
height = 100
wt = 2

print(f"Params: {width=} {depth=} {height=} {wt=}")

outer_cube = cube([width, depth, height])
inner_cube = cube([width-2*wt, depth-2*wt, height-wt+0.1])
inner_cube = translate([wt, wt, wt])(inner_cube)

hollow_cube = outer_cube - inner_cube
scad_render_to_file(hollow_cube, 'box.scad')
