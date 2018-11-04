from PIL import Image
from reconstruct_from_run_forest import *
import argparse

def decrement_column_indices(col, l):
    for (i, run) in enumerate(col):
        col[i] = (run[0] - l), (run[1] - l)
    return col

def remove_null_runs(upper, lower):
    if (upper[-1][0] == upper[-1][1]):
        upper = upper[:-1]
    if (lower[0][0] == lower[0][1]):
        lower = lower[1:]
    return (upper, lower)

def split_column(col, l):
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
    n_rows, n_cols = rf[0]
    rf_cols = rf[1]

    split_im_dims = n_rows, int(n_cols/2)

    l_rf_cols, r_rf_cols = rf_cols[:int(n_cols/2)], rf_cols[int(n_cols/2):]
    l_rf, r_rf = (split_im_dims, l_rf_cols), (split_im_dims, r_rf_cols)
    return(l_rf, r_rf)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    rf_path = args.rf_path

    rf = parse_run_forest_file(rf_path)

    left_rf, right_rf = vert_split_rf(rf)

    bin_left = run_forest_to_binary(left_rf)
    bin_right = run_forest_to_binary(right_rf)

    upper_rf, lower_rf = horz_split_rf(rf)

    bin_upper = run_forest_to_binary(upper_rf)
    bin_lower = run_forest_to_binary(lower_rf)

    Image.fromarray(bin_upper * 255).show()
    Image.fromarray(bin_lower * 255).show()

if __name__ == '__main__':
    main()

