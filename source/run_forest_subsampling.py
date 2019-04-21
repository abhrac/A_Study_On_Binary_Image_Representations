import argparse
from utils.parse_utils import *
from utils.save_utils import *

from reconstruct_from_run_forest import *

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

def get_subsample_value(rf_cols, row, col, factor):
    num_ones = 1
    for i in range(row, (row+factor)):
        for j in range(col, col+factor):
            if (rf_index(rf_cols, i, j) == 1):
                num_ones = num_ones + 1
    return (num_ones > (factor ** 2))

def get_end_index(rf_cols, col, start, height, factor):
    end = (start // factor) + 1
    for i in range((start+factor), height, factor):
        subsample_value = get_subsample_value(rf_cols, i, col, factor)
        if (subsample_value == 1):
            end = end + 1
        else:
            return end
    return end

def subsample_run_forest(run_forest, factor):
    (height, width), rf_cols = run_forest
    subsample_cols = []
    for j in range(0, width, factor):
        subsample_col = []
        i = 0
        while (i < height):
            subsample_value = get_subsample_value(rf_cols, i, j, factor)
            if (subsample_value == 1):
                end = get_end_index(rf_cols, j, i, height, factor)
                subsample_col.append(((i//factor), end))
                i = (end * factor) + 1
                continue
            i = i + factor
        subsample_cols.append(subsample_col)
    return ((((height//factor), (width//factor)), subsample_cols))

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    return parser.parse_args().rf_path

def main():
    rf_path = get_arguments()

    run_forest = parse_run_forest_file(rf_path)

    subsampled_rf = subsample_run_forest(run_forest, 4)

    subsampled_rf_bin = run_forest_to_binary(subsampled_rf)

    save_run_forest(subsampled_rf, rf_path, suffix='_subsampled',
            target_path='../run_forest_representations/subsampled/')
    save_image(subsampled_rf_bin, rf_path, im_prefix='subsampled_',
            im_path='../reconstructed_images/subsampled/')

    Image.fromarray(run_forest_to_binary(run_forest) * 255).show()
    Image.fromarray(subsampled_rf_bin * 255).show()

    return 0

if __name__ == '__main__':
    main()

