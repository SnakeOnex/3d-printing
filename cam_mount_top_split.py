import os
from solid import *
from solid.utils import *

camera_pole = import_stl(
    "../SO-ARM100/Optional/Overhead_Cam_Mount_Webcam/stl/cam_mount_top.stl"
)

# 1. center the pole
# camera_pole = translate([-37.4 / 2, 0, -73.025 / 2])(camera_pole)

scad_render_to_file(camera_pole, f"cam_mount_top.scad")

# 2. cut it into two pieces
full_depth = 242.45
mask_w, mask_d, mask_h = 50, full_depth / 2, 100
first_piece_mask = cube([mask_w, mask_d, mask_h])
first_piece_mask = translate([-mask_w / 2, 0, -mask_h / 2])(first_piece_mask)
second_piece_mask = translate([0, full_depth / 2, 0])(first_piece_mask)
camera_pole_bottom = camera_pole * first_piece_mask
camera_pole_toppom = camera_pole * second_piece_mask

# 2.a create a cavity
tol = 0.2
conn_w, conn_d, conn_h = 20, 50, 30
d_trans = full_depth / 2 - conn_d
print(f"{conn_w=} {conn_d=} {conn_h=} {d_trans=}")
cavity_w, cavity_d, cavity_h = conn_w + tol, conn_d + tol, conn_h + tol
exten_w, exten_d, exten_h = conn_w - tol, conn_d, conn_h + tol
cavity_d_trans, exten_d_trans = d_trans - tol, d_trans
cavity_block = cube([cavity_w, cavity_d, cavity_h])
cavity_block = translate([-cavity_w / 2, cavity_d_trans, -cavity_h / 2])(cavity_block)

camera_pole_bottom -= cavity_block

# 2.b create a extension
extension_block = cube([exten_w, exten_d, exten_h])
extension_block = translate([-exten_w / 2, exten_d_trans, -exten_h / 2])(
    extension_block
)
camera_pole_toppom += extension_block
camera_pole_toppom = translate([0, -exten_d_trans, 0])(camera_pole_toppom)


scad_render_to_file(camera_pole_bottom, f"cam_mount_top_bot.scad")
scad_render_to_file(camera_pole_toppom, f"cam_mount_top_top.scad")

os.system(f"openscad -o cam_mount_top_bot.stl cam_mount_top_bot.scad")
os.system(f"openscad -o cam_mount_top_top.stl cam_mount_top_top.scad")
