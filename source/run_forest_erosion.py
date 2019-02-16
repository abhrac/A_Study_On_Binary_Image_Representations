from utils.parse_utils import *
from utils.save_utils import *
from reconstruct_from_run_forest import *
import numpy as np
import argparse

def get_structuring_element():
    struct_elm = np.ones((11, 11))
    return struct_elm

def rf_index(rf_cols, i, j):
    col = rf_cols[j]
    for run in col:
        if (run != []):
            start, end = run
            if ((i >= start) and (i < end)):
                return 1
    return 0

def has_background(rf_cols, x, y, struct_elm):
    se_height, se_width = struct_elm.shape
    for i in range(se_height):
        for j in range(se_width):
            im_pixel = rf_index(rf_cols, (x+i), (y+j))
            if ((im_pixel == 0) and (struct_elm[i, j] == 1)):
                return True
    return False

def invert_pixel(rf_cols, i, j):
    col = rf_cols[j]
    for (k, run) in enumerate(col):
        if (run != []):
            start, end = run
            if ((i >= start) and (i < end)):
                replacement_runs = [(start, i), ((i+1), end)]
                if (i == start):
                    replacement_runs = replacement_runs[1:]
                if ((i+1) == end):
                    replacement_runs = replacement_runs[:-1]
                col = col[0 : k] + replacement_runs + col[(k+1) : ]
                break
    rf_cols[j] = col
    return rf_cols

def erode_run_forest(run_forest, struct_elm):
    im_height, im_width = run_forest[0]
    rf_cols = run_forest[1]
    se_height, se_width = struct_elm.shape
    vert_range, horz_range = (im_height-se_height), (im_width-se_width)
    eroded_rf_cols = rf_cols.copy()
    for i in range(vert_range):
        for j in range(horz_range):
            center_x, center_y = (i+(se_height//2)), (j+(se_width//2))
            center = rf_index(rf_cols, center_x, center_y)
            if (center == 1):
                if (has_background(rf_cols, i, j, struct_elm)):
                    eroded_rf_cols = invert_pixel(eroded_rf_cols, center_x, center_y)
    return eroded_rf_cols

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    return args.rf_path

def main():
    rf_path = parse_arguments()
    run_forest = parse_run_forest_file(rf_path)
    struct_elm = get_structuring_element()

    eroded_rf_cols = erode_run_forest(run_forest, struct_elm)
    eroded_rf = run_forest[0], eroded_rf_cols

    save_run_forest(eroded_rf, rf_path, suffix='_eroded', target_path='../run_forest_representations/eroded/')

    eroded_rf_bin = run_forest_to_binary(eroded_rf)
    save_image(eroded_rf_bin, rf_path, im_prefix='eroded_', im_path='../reconstructed_images/eroded/')
    Image.fromarray(eroded_rf_bin * 255).show()

    return 0

if __name__ == '__main__':
    main()

