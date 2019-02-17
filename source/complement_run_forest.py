from utils.parse_utils import *
from utils.save_utils import *
from reconstruct_from_run_forest import *
from PIL import Image
import numpy as np
import argparse

def complement_run_forest(run_forest):
    rf_dims, rf_cols = run_forest
    rf_cols_prime = []
    for col in rf_cols:
        col_prime = []
        num_runs, prev_end = len(col), 0
        if (num_runs == 0):
            rf_cols_prime.append([(0, rf_dims[0])])
            continue
        for (i, run) in enumerate(col):
            start, end = run
            if ((i == 0) and (start != 0)):
                col_prime.append((0, start))
            else:
                col_prime.append((prev_end, start))
            prev_end = end
        if (prev_end != rf_dims[0]):
            col_prime.append((prev_end, rf_dims[0]))
        rf_cols_prime.append(col_prime)
    return (rf_dims, rf_cols_prime)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    return args.rf_path

def main():
    rf_path = get_arguments()
    run_forest = parse_run_forest_file(rf_path)

    rf_prime = complement_run_forest(run_forest)
    save_run_forest(rf_prime, rf_path, suffix='_complement',
                    target_path='../run_forest_representations/complemented/')

    bin_im_prime = run_forest_to_binary(rf_prime)
    Image.fromarray(bin_im_prime * 255).show()

if __name__ == '__main__':
    main()

