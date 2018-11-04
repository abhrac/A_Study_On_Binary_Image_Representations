from split_run_forests import *
from reconstruct_from_quadtree import *
from utils.parse_utils import *
from utils.save_utils import *
import argparse

def has_multiple_runs(col):
    return (len(col) > 1)

def run_spans_column(col, col_len):
    if ((len(col) == 0)):
        return True
    return ((col[0][1] - col[0][0]) == col_len)

def uniform_columns(cols):
    col_0 = cols[0]
    for col in cols:
        if (col != col_0):
            return False
    return True

def color(col):
    return (len(col)> 0)

def test_homogeneity(rf):
    col_0 = rf[1][0]
    if (has_multiple_runs(col_0)):
        return (False, -1)
    if (not uniform_columns(rf[1])):
        return (False, -1)
    if (not run_spans_column(col_0, rf[0][0])):
        return (False, -1)
    return(True, color(col_0))

def recursively_decompose_rf(rf, code, leaves):
    homogeneous, color = test_homogeneity(rf)
    if (homogeneous):
        leaves.append((code, (color * 1)))
        return leaves

    upper_half, lower_half = horz_split_rf(rf)

    quad_0, quad_1 = vert_split_rf(upper_half)
    quad_2, quad_3 = vert_split_rf(lower_half)

    leaves = recursively_decompose_rf(quad_0, (code + '0'), leaves)
    leaves = recursively_decompose_rf(quad_1, (code + '1'), leaves)
    leaves = recursively_decompose_rf(quad_2, (code + '2'), leaves)
    leaves = recursively_decompose_rf(quad_3, (code + '3'), leaves)
    return leaves

def run_forest_to_quadtree(rf):
    leaves = recursively_decompose_rf(rf, '0', [])
    return (rf[0], leaves)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    rf_path = args.rf_path

    rf = parse_run_forest_file(rf_path)
    
    quadtree = run_forest_to_quadtree(rf)
    
    target_path = '../quadtree_codes/from_run_forests/'
    
    qt_code_path = save_quadtree_codes(rf_path, quadtree, target_path)

    quadtree = parse_qt_code_file(qt_code_path)

    reconstructed_im = quadtree_to_binary(quadtree)

    Image.fromarray(reconstructed_im * 255).show()

    target_path = '../reconstructed_images/run_forest_to_quadtree/'

    im_prefix = 'rf_to_qt_'

    save_reconstructed_im(reconstructed_im, qt_code_path, target_path, im_prefix)

if __name__ == '__main__':
    main()

