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

def get_expansion_block(value, factor, start, end):
    if (value == 1):
        return [[(start, end)] for i in range(factor)]
    return [[] for i in range(factor)]

def fuse_blocks(expansion_blocks, factor):
    fused_col = []
    for block in expansion_blocks:
        if ((fused_col == []) or (block[0] == []) or (fused_col[-1][1] != block[0][0][0])):
            fused_col.extend(block[0])
        else:
            start, end = fused_col[-1][0], block[0][0][1]
            fused_col[-1] = (start, end)
    return ([fused_col] * factor)

def zoom_run_forest(run_forest, factor):
    (height, width), rf_cols = run_forest
    zoomed_cols = []
    for j in range(0, width):
        expansion_blocks = []
        for i in range(0, height):
            value = rf_index(rf_cols, i, j)
            start, end = (i * factor), ((i+1) * factor)
            expansion_blocks.append(get_expansion_block(value, factor, start, end))
        fused_expansion_blocks = fuse_blocks(expansion_blocks, factor)
        zoomed_cols.extend(fused_expansion_blocks)
    return (((height*factor), (width*factor)), zoomed_cols)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    return parser.parse_args().rf_path

def main():
    rf_path = get_arguments()

    run_forest = parse_run_forest_file(rf_path)

    zoomed_rf = zoom_run_forest(run_forest, 4)

    zoomed_rf_bin = run_forest_to_binary(zoomed_rf)

    save_run_forest(zoomed_rf, rf_path, suffix='_zoomed',
            target_path='../run_forest_representations/zoomed/')
    save_image(zoomed_rf_bin, rf_path, im_prefix='zoomed_',
            im_path='../reconstructed_images/zoomed/')

    Image.fromarray(run_forest_to_binary(run_forest) * 255).show()
    Image.fromarray(zoomed_rf_bin * 255).show()

    return 0

if __name__ == '__main__':
    main()

