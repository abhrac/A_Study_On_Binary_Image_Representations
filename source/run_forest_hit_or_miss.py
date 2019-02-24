from reconstruct_from_run_forest import *
from run_forest_union import *
from utils.parse_utils import *
from utils.save_utils import *
import numpy as np
import argparse

def rf_index(rf_cols, x, y):
    col = rf_cols[y]
    if col == []:
        return 0
    for run in col:
        if ((x >= run[0]) and (x < run[1])):
            return 1
        if (x < run[0]):
            return 0
    return 0

def matches(rf_cols, x, y, struct_elm):
    se_height, se_width = struct_elm.shape
    for i in range(se_height):
        for j in range(se_width):
            if (rf_index(rf_cols, (x+i), (y+j)) != struct_elm[i, j]):
                return False
    return True

def invert_pixel(rf_cols, x, y):
    runs = rf_cols[y]
    for (k, run) in enumerate(runs):
        start, end = run
        if ((x >= start) and (x < end)):
            replacement_runs = [(start, x), ((x+1), end)]
            if (x == start):
                replacement_runs = replacement_runs[1:]
            if (x == (end-1)):
                replacement_runs = replacement_runs[:-1]
            runs = runs[: k] + replacement_runs + runs[(k+1) : ]
            break
    rf_cols[y] = runs
    return rf_cols

def hit_or_miss(run_forest, struct_elm):
    im_height, im_width = run_forest[0]
    rf_cols = run_forest[1]
    se_height, se_width = struct_elm.shape
    vert_range, horz_range = (im_height-se_height), (im_width-se_width)
    out_rf_cols = rf_cols.copy()
    for i in range(vert_range):
        for j in range(horz_range):
            center_x, center_y = (i+(se_height//2)), (j+(se_width//2))
            center = rf_index(rf_cols, center_x, center_y)
            if (center == 1):
                if (not matches(rf_cols, i, j, struct_elm)):
                    out_rf_cols = invert_pixel(out_rf_cols, center_x, center_y)
    return (run_forest[0], out_rf_cols)

def vertical_structuring_element():
    struct_elm = (np.zeros((3, 3)), np.zeros((3, 3)))
    struct_elm[0][:, 1:] = 1
    struct_elm[1][:, :2] = 1
    return struct_elm

def horizontal_structuring_element():
    struct_elm = (np.zeros((3, 3)), np.zeros((3, 3)))
    struct_elm[0][1:, :] = 1
    struct_elm[1][:2, :] = 1
    return struct_elm

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    return args.rf_path

def vertical_edges_run_forest(run_forest, vert_struct_elm):
    left_edges_rf = hit_or_miss(run_forest, vert_struct_elm[0])
    right_edges_rf = hit_or_miss(run_forest, vert_struct_elm[1])
    vert_edges_rf = run_forest_union(left_edges_rf, right_edges_rf)
    return vert_edges_rf

def horizontal_edges_run_forest(run_forest, horz_struct_elm):
    top_edges_rf = hit_or_miss(run_forest, horz_struct_elm[0])
    bottom_edges_rf = hit_or_miss(run_forest, horz_struct_elm[1])
    horz_edges_rf = run_forest_union(top_edges_rf, bottom_edges_rf)
    return horz_edges_rf

def display_detected_edges(run_forest, vert_edges_bin, horz_edges_bin, edges_bin):
    Image.fromarray(run_forest_to_binary(run_forest) * 255).show()
    Image.fromarray(vert_edges_bin * 255).show()
    Image.fromarray(horz_edges_bin * 255).show()
    Image.fromarray(edges_bin * 255).show()
    return 0

def main():
    rf_path = get_arguments()
    run_forest = parse_run_forest_file(rf_path)
    
    vert_struct_elm = vertical_structuring_element()
    horz_struct_elm = horizontal_structuring_element()
    
    vert_edges_rf = vertical_edges_run_forest(run_forest, vert_struct_elm)
    horz_edges_rf = horizontal_edges_run_forest(run_forest, horz_struct_elm)
    
    edges_rf = run_forest_union(vert_edges_rf, horz_edges_rf)
    save_run_forest(edges_rf, rf_path, suffix='_hit_or_miss',
                    target_path='../run_forest_representations/hit_or_miss/')

    vert_edges_bin = run_forest_to_binary(vert_edges_rf)
    horz_edges_bin = run_forest_to_binary(horz_edges_rf)
    edges_bin = run_forest_to_binary(edges_rf)

    save_image(edges_bin, rf_path, im_prefix='hit_or_miss_',
                im_path='../reconstructed_images/hit_or_miss/')
    display_detected_edges(run_forest, vert_edges_bin, horz_edges_bin, edges_bin)

    return 0

if __name__ == '__main__':
    main()

