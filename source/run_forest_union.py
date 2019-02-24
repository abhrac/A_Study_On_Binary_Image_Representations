from utils.parse_utils import *
from utils.save_utils import *
from reconstruct_from_run_forest import *
import argparse

def merge_runs(run1, run2):
    start = min(run1[0], run2[0])
    end = max(run1[1], run2[1])
    return (start, end)

def append_run(runs, run):
    if (runs == []):
        return [run]
    last_run = runs[-1]
    if (run[0] < last_run[1]):
        end = max(run[1], last_run[1])
        runs[-1] = (runs[-1][0], end)
        return runs
    runs.append(run)
    return (runs)

def disjoint(pair):
    run1, run2 = pair
    if ((run2[0] <= run1[0] < run2[1]) or (run1[0] <= run2[0] < run1[1])):
        return False
    return True

def append_runs(u_col, run1, run2):
    pair = sorted([run1, run2])
    if (not disjoint(pair)):
        merged_run = merge_runs(run1, run2)
        u_col = append_run(u_col, merged_run)
    else:
        u_col = append_run(u_col, pair[0])
        u_col = append_run(u_col, pair[1])
    return u_col

def merge_non_null_columns(col1, col2):
    u_col = []
    l_col1, l_col2 = len(col1), len(col2)
    max_runs = max(l_col1, l_col2)
    for j in range(max_runs):
        if (j >= l_col1):
            u_col = append_run(u_col, col2[j])
        elif (j >= l_col2):
            u_col = append_run(u_col, col1[j])
        else:
            u_col = append_runs(u_col, col1[j], col2[j])
    return u_col

def run_forest_union(rf1, rf2):
    rf1_dims, rf1_cols = rf1
    rf2_dims, rf2_cols = rf2
    assert (rf1_dims == rf2_dims)
    u_rf_cols = []
    for i in range(rf1_dims[1]):
        col1, col2 = rf1_cols[i], rf2_cols[i]
        if (col1 == []):
            u_rf_cols.append(col2)
        elif (col2 == []):
            u_rf_cols.append(col1)
        else:
            u_col = merge_non_null_columns(col1, col2)
            u_rf_cols.append(u_col)
    return (rf1_dims, u_rf_cols)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf1_path', type=str)
    parser.add_argument('rf2_path', type=str)
    args = parser.parse_args()
    return (args.rf1_path, args.rf2_path)

def main():
    rf1_path, rf2_path = get_arguments()
    rf1 = parse_run_forest_file(rf1_path)
    rf2 = parse_run_forest_file(rf2_path)

    u_rf = run_forest_union(rf1, rf2)
    save_run_forest(u_rf, rf1_path, suffix='_union',
                    target_path='../run_forest_representations/union/')

    u_bin = run_forest_to_binary(u_rf)
    save_image(u_bin, rf1_path, im_prefix='union_',
               im_path='../reconstructed_images/union/')
    Image.fromarray(u_bin * 255).show()

    return 0

if __name__ == '__main__':
    main()

