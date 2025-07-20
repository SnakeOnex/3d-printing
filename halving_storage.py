import os
from solid import *
from solid.utils import *

def halving_box(w, d, h, wt=1.5, tol=0.2):
    while True:
        iw = w - 2 * wt
        id = d - 2 * wt
        ih = h - wt

        outer_cube = cube([w, d, h])
        inner_cube = cube([iw+tol, id+tol, ih])
        inner_cube = translate([wt-tol/2, wt-tol/2, wt])(inner_cube)

        hollow_box = outer_cube - inner_cube
        yield hollow_box, {"w":w, "d":d, "h":h, "iw":iw, "id":id, "ih":ih}

        if w >= d: w, d = iw / 2, id
        else: w, d = iw, id / 2

gen = halving_box(160, 160, 30)

i = 0
while True:
    box, deb = next(gen)
    if min(deb["iw"], deb["ih"]) < 20: break
    scad_render_to_file(box, f"l{i}_recur_storage.scad")
    print(f"saved l{i}_recur_storage.scad of size: {deb}")
    os.system(f"openscad -o l{i}_recur_storage.stl l{i}_recur_storage.scad")
    i += 1
