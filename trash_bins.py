import os
from solid import *
from solid.utils import *


def make_trash_bin(
    w,
    h,
    bottom_stacking=True,
    bottom_type="male",
    top_stacking=True,
    top_type="male",
    horizontal_stacking=True,
    wt=4.0,
    tol=0.2,
):
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

    # female fin cube
    fin_cube_inner = cube([fin_outer_size + tol, fin_outer_size + tol, fin_h])
    fin_cube_inner = translate([wt - fin_w - tol / 2, wt - fin_w - tol / 2, 0])(
        fin_cube_inner
    )

    # male fin cube
    fin_cube_outer = cube([w, w, fin_h]) - fin_cube_inner

    if top_stacking:
        fin_cube_top = translate([0, 0, h - fin_h])(
            fin_cube_inner if top_type == "male" else fin_cube_outer
        )
        hollow_box = hollow_box - fin_cube_top

    # 3. add connect fins to the bottom
    if bottom_stacking:
        fin_cube_bottom = translate([0, 0, 0])(
            fin_cube_inner if top_type == "male" else fin_cube_outer
        )
        hollow_box = hollow_box - fin_cube_bottom

    # 4. add protrusion for horizontal stacking
    if horizontal_stacking:
        protrusion_length = 10
        protrusion_w = 1.0
        clip_length = 2.0

        protrusion = cube([protrusion_length, protrusion_w, h])
        clippy_part_male = cube([clip_length - 0.1, protrusion_w - 0.1, h])
        clippy_part_female = cube([clip_length + 0.1, protrusion_w + 0.1, h])

        clippy_part_male = translate([protrusion_length, 0, 0])(
            rotate([0, 0, 90])(clippy_part_male)
        )
        clippy_part_female = translate([protrusion_length, 0, 0])(
            rotate([0, 0, 90])(clippy_part_female)
        )
        protrusion_positive = protrusion + clippy_part_male
        protrusion_negative = protrusion + clippy_part_female

        # a. add the extended wall with a clippy part
        protrusion_rotated = rotate([0, 0, -90])(protrusion_positive)
        hollow_box = hollow_box + protrusion_rotated

        # b. add the cavity in the wall with a hole
        protrusion_rotated = rotate([0, 0, 180])(protrusion_negative)
        protrusion_rotated = translate([w, w, 0])(protrusion_rotated)
        hollow_box = hollow_box - protrusion_rotated

    return hollow_box, {"w": w, "h": h, "iw": iw, "ih": ih}


width, height = 40, 20

trash_bin_bottom, debug = make_trash_bin(
    width, height, bottom_stacking=False, top_stacking=True, top_type="male"
)
scad_render_to_file(trash_bin_bottom, f"trash_bin_bottom.scad")

trash_bin_middle, debug = make_trash_bin(
    width,
    height,
    bottom_stacking=True,
    bottom_type="female",
    top_stacking=True,
    top_type="female",
)
scad_render_to_file(trash_bin_middle, f"trash_bin_middle.scad")

trash_bin_top, debug = make_trash_bin(
    width,
    height,
    bottom_stacking=True,
    bottom_type="male",
    top_stacking=False,
)
scad_render_to_file(trash_bin_top, f"trash_bin_top.scad")

os.system(f"openscad -o trash_bin_bottom.stl trash_bin_bottom.scad")
os.system(f"openscad -o trash_bin_middle.stl trash_bin_middle.scad")
os.system(f"openscad -o trash_bin_top.stl trash_bin_top.scad")
