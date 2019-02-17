from utils.parse_utils import *
from utils.save_utils import *
from complement_run_forest import *
from run_forest_erosion import *
from reconstruct_from_run_forest import *
import argparse

def get_structuring_element():
    return np.ones((11, 11))

def dilate(run_forest, struct_elm):
    rf_prime = complement_run_forest(run_forest)
    eroded_rf_prime = erode_run_forest(rf_prime, struct_elm)
    dilated_rf = complement_run_forest(eroded_rf_prime)
    return dilated_rf

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    return args.rf_path

def main():
    rf_path = get_arguments()
    run_forest = parse_run_forest_file(rf_path)

    struct_elm = get_structuring_element()

    dilated_rf = dilate(run_forest, struct_elm)
    dilated_bin = run_forest_to_binary(dilated_rf)

    save_run_forest(dilated_rf, rf_path, suffix='_dilated',
                    target_path='../run_forest_representations/dilated/')
    save_image(dilated_bin, rf_path, im_prefix='dilated_',
                im_path='../reconstructed_images/dilated/')
    Image.fromarray(dilated_bin * 255).show()

    return 0


if __name__ == '__main__':
    main()

