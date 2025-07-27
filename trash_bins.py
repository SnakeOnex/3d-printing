import os
from solid import *
from solid.utils import *


def make_trash_bin(w, h, bottom_stacking=True, top_stacking=True, wt=2.0, tol=0.2):
    iw = w - 2 * wt
    ih = h - wt

    # 1. main body
    outer_cube = cube([w, w, h])

    if bottom_stacking:
        inner_cube = cube([iw, iw, h])
        inner_cube = translate([wt, wt, 0])(inner_cube)
    else:
        inner_cube = cube([iw, iw, ih])
        inner_cube = translate([wt, wt, wt])(inner_cube)

    hollow_box = outer_cube - inner_cube

    # 2. make the box vertically stackable (add fins to the top of the box)
    fin_w, fin_h = 1.0, 5.0
    fin_outer_size = iw + 2 * fin_w
    if top_stacking:
        fin_cube = cube([fin_outer_size + tol, fin_outer_size + tol, fin_h])
        fin_cube = translate([wt - fin_w - tol / 2, wt - fin_w - tol / 2, h - fin_h])(
            fin_cube
        )
        hollow_box = hollow_box - fin_cube

    # 3. add connect fins to the bottom
    if bottom_stacking:
        fin_cube_bottom = cube([fin_outer_size + tol, fin_outer_size + tol, fin_h])
        fin_cube_bottom = translate([wt - fin_w - tol / 2, wt - fin_w - tol / 2, 0])(
            fin_cube_bottom
        )
        hollow_box = hollow_box - fin_cube_bottom

    return hollow_box, {"w": w, "h": h, "iw": iw, "ih": ih}


width, height = 40, 40

trash_bin_bottom, debug = make_trash_bin(width, height, bottom_stacking=False)
scad_render_to_file(trash_bin_bottom, f"trash_bin_bottom.scad")

trash_bin_middle, debug = make_trash_bin(
    width, height, bottom_stacking=True, top_stacking=True
)
scad_render_to_file(trash_bin_middle, f"trash_bin_middle.scad")

trash_bin_top, debug = make_trash_bin(
    width, height, bottom_stacking=True, top_stacking=False
)
scad_render_to_file(trash_bin_top, f"trash_bin_top.scad")

os.system(f"openscad -o trash_bin_bottom.stl trash_bin_bottom.scad")
os.system(f"openscad -o trash_bin_middle.stl trash_bin_middle.scad")
os.system(f"openscad -o trash_bin_top.stl trash_bin_top.scad")
