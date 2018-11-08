# Program to vertically and horizontally split a given run-forest
# Usage: python split_run_forests.py path_to_run_forest_file 
# Example: python split_run_forests.py ../run_forest_representations/1024x1024/scenery_1_1024x1024_run_forest.txt

from PIL import Image
from reconstruct_from_run_forest import *
import argparse

def decrement_column_indices(col, l):
    # Function to decrement the run indices of col by l
    for (i, run) in enumerate(col):
        col[i] = (run[0] - l), (run[1] - l)
    return col

def remove_null_runs(upper, lower):
    # Function to remove runs that start and end in
    # the same pixel
    if (upper[-1][0] == upper[-1][1]):
        upper = upper[:-1]
    if (lower[0][0] == lower[0][1]):
        lower = lower[1:]
    return (upper, lower)

def split_column(col, l):
    # Function to split a run-forest column into 2 halves
    mid = int(l / 2)
    for (i, run) in enumerate(col):
        if (run[0] <= mid <= run[1]):
            upper = col[:i] + [(run[0], mid)]
            lower = [(mid, run[1])] + col[(i + 1):]
            upper, lower = remove_null_runs(upper, lower)
            decrement_column_indices(lower, mid)
            return(upper, lower)
        if (mid < run[0]):
            upper = col[:i]
            lower = decrement_column_indices(col[i:], mid)
            return(upper, lower)
    upper = col[:mid]
    lower = decrement_column_indices(col[mid:], mid)
    return(upper, lower)

def horz_split_rf(rf):
    # Function to horizontally split a run-forest
    n_rows, n_cols = rf[0]
    rf_cols = rf[1]
    split_im_dims = int(n_rows / 2), n_cols
    u_rf_cols, l_rf_cols = [], []
    for col in rf_cols:
        upper, lower = split_column(col, n_rows)
        u_rf_cols.append(upper)
        l_rf_cols.append(lower)
    u_rf, l_rf = (split_im_dims, u_rf_cols), (split_im_dims, l_rf_cols)
    return (u_rf, l_rf)

def vert_split_rf(rf):
    # Function to vertically split a run-forest
    n_rows, n_cols = rf[0]
    rf_cols = rf[1]
    split_im_dims = n_rows, int(n_cols/2)
    l_rf_cols, r_rf_cols = rf_cols[:int(n_cols/2)], rf_cols[int(n_cols/2):]
    l_rf, r_rf = (split_im_dims, l_rf_cols), (split_im_dims, r_rf_cols)
    return(l_rf, r_rf)

def get_rf_path_from_arguments():
    # Function to parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    return args.rf_path

def binarize_all(run_forests):
    # Function to convert a list of run-forests to their
    # corresponding binary images
    bin_ims = []
    for rf in run_forests:
        bin_ims.append(run_forest_to_binary(rf))
    return (bin_ims)

def display_binary_images(images):
    # Function to display a list of binary images
    for im in images:
        Image.fromarray(im * 255).show()

def main():
    # Get path to run-forest file from command-line arguments
    rf_path = get_rf_path_from_arguments()

    # Get run-forest file from parsed command-line arguments
    rf = parse_run_forest_file(rf_path)
    
    # Split the given run-forest vertically
    left_rf, right_rf = vert_split_rf(rf)
    
    # Split the given run-forest horizontally
    upper_rf, lower_rf = horz_split_rf(rf)
    
    # Get corresponding binary images from the horizontally
    # split run-forests
    bin_left, bin_right, bin_upper, bin_lower = binarize_all([left_rf, right_rf, upper_rf, lower_rf])

    # Display images obtained from vertical and horizontal splitting
    display_binary_images([bin_left, bin_right, bin_upper, bin_lower])

if __name__ == '__main__':
    main()

