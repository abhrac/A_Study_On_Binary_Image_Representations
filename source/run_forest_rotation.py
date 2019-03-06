from utils.parse_utils import *
from utils.save_utils import *
from reconstruct_from_run_forest import *
import argparse

def rf_index(rf_cols, i, j):
    col = rf_cols[j]
    for run in col:
        if (run != []):
            start, end = run
            if (start > i):
                return 0
            if ((i >= start) and (i < end)):
                return 1
    return 0

def get_end_index_reverse(rf_cols, i, start):
    num_cols = len(rf_cols)
    end = start - 1
    while ((end >= 0) and (rf_index(rf_cols, i, end) == 1)):
        end = end - 1
    return end

def rotate_anticlockwise(run_forest):
    rf_dims, rf_cols = run_forest
    rotated_rf_cols = []
    for i in range(rf_dims[0]):
        col, j = [], (rf_dims[1]-1)
        while j >= 0:
            pixel_value = rf_index(rf_cols, i, j)
            if (pixel_value == 1):
                start = j
                end = get_end_index_reverse(rf_cols, i, start)
                start_prime, end_prime = (rf_dims[1]-1-start), (rf_dims[1]-1-end)
                col.append((start_prime, end_prime))
                j = end
            j = j - 1
        rotated_rf_cols.append(col)
    return (rf_dims, rotated_rf_cols)

def get_end_index(rf_cols, i, start):
    num_cols = len(rf_cols)
    end = start + 1
    while ((end < num_cols) and (rf_index(rf_cols, i, end) == 1)):
        end = end + 1
    return end

def rotate_clockwise(run_forest):
    rf_dims, rf_cols = run_forest
    rotated_rf_cols = []
    for i in range(rf_dims[0], 0, -1):
        col, j = [], 0
        while (j < rf_dims[1]):
            pixel_value = rf_index(rf_cols, i, j)
            if (pixel_value == 1):
                start = j
                end = get_end_index(rf_cols, i, start)
                col.append((start, end))
                j = end
            j = j + 1
        rotated_rf_cols.append(col)
    return (rf_dims, rotated_rf_cols)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    return args.rf_path

def main():
    rf_path = get_arguments()
    run_forest = parse_run_forest_file(rf_path)
    
    clockwise_rotated_rf = rotate_clockwise(run_forest)
    clockwise_rotated_rf_bin = run_forest_to_binary(clockwise_rotated_rf)

    anticlockwise_rotated_rf = rotate_anticlockwise(run_forest)
    anticlockwise_rotated_rf_bin = run_forest_to_binary(anticlockwise_rotated_rf)

    save_run_forest(clockwise_rotated_rf, rf_path, suffix='_clockwise_rotated',
            target_path='../run_forest_representations/rotated/')
    save_image(clockwise_rotated_rf_bin, rf_path, im_prefix='clockwise_rotated_',
            im_path='../reconstructed_images/rotated/')
 
    save_run_forest(anticlockwise_rotated_rf, rf_path, suffix='_anticlockwise_rotated',
            target_path='../run_forest_representations/rotated/')
    save_image(anticlockwise_rotated_rf_bin, rf_path, im_prefix='anticlockwise_rotated_',
            im_path='../reconstructed_images/rotated/')
       
    Image.fromarray(clockwise_rotated_rf_bin * 255).show()
    Image.fromarray(anticlockwise_rotated_rf_bin * 255).show()

    return 0

if __name__ == '__main__':
    main()

