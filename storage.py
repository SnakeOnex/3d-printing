from solid import *
from solid.utils import *

def box(inner_width, inner_height, wt=2.0, tol=0.3):
    outer_width = inner_width + 2 * wt
    outer_height = inner_height + wt

    outer_cube = cube([outer_width, outer_width, outer_height])
    inner_cube = cube([inner_width+tol, inner_width+tol, inner_height])
    inner_cube = translate([wt, wt, wt])(inner_cube)
    
    hollow_box = outer_cube - inner_cube
    return hollow_box, (outer_width, outer_height)

l1_w = 20.0
l1_h = 10.0
l1_box, (l1_ow, _)  = box(l1_w, l1_h)
print(f"{l1_w=} {l1_ow=}")

l2_w = 2*l1_ow
l2_h = 20.0
l2_box, (l2_ow, _)  = box(l2_w, l2_h)
print(f"{l2_w=} {l2_ow=}")

l3_w = 2*l2_ow
l3_h = 30.0
l3_box, (l3_ow, _)  = box(l3_w, l3_h)
print(f"{l3_w=} {l3_ow=}")

scene = l1_box + translate([60, 0, 0])(l2_box) + translate([220, 0, 0])(l3_box)

scad_render_to_file(scene, "recursive_boxes.scad")

scad_render_to_file(l1_box, "level1_box.scad")
scad_render_to_file(l2_box, "level2_box.scad")
scad_render_to_file(l3_box, "level3_box.scad")

