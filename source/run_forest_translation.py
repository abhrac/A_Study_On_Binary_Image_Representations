from utils.parse_utils import *
from utils.save_utils import *
from reconstruct_from_run_forest import *
import argparse

def translate_vertically(run_forest, translation_factor):
    rf_dims, rf_cols = run_forest
    translated_cols = []
    for col in rf_cols:
        translated_col = []
        for run in col:
            translated_start = run[0] + translation_factor
            translated_end = run[1] + translation_factor
            if (translated_start >= rf_dims[1]):
                break
            if (translated_end > rf_dims[1]):
                translated_col.append((translated_start, rf_dims[1]))
                break
            translated_col.append((translated_start, translated_end))
        translated_cols.append(translated_col)
    return (rf_dims, translated_cols)

def translate_horizontally(run_forest, translation_factor):
    rf_dims, rf_cols = run_forest
    num_valid_columns = rf_dims[1] - translation_factor
    valid_columns = rf_cols[ : num_valid_columns]
    translation_pad = [[] for i in range(translation_factor)]
    translated_rf_cols = translation_pad + valid_columns
    return (rf_dims, translated_rf_cols)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('rf_path', type=str)
    args = parser.parse_args()
    return args.rf_path

def main():
    rf_path = get_arguments()
    run_forest = parse_run_forest_file(rf_path)
    translation_factor = 100
    
    horz_translated_rf = translate_horizontally(run_forest, translation_factor)
    vert_translated_rf = translate_vertically(run_forest, translation_factor)

    save_run_forest(horz_translated_rf, rf_path, suffix='_horizontally_translated',
            target_path='../run_forest_representations/translated/')
    
    save_run_forest(vert_translated_rf, rf_path, suffix='_vertically_translated',
            target_path='../run_forest_representations/translated/')

    horz_translated_rf_bin = run_forest_to_binary(horz_translated_rf)
    vert_translated_rf_bin = run_forest_to_binary(vert_translated_rf)

    save_image(horz_translated_rf_bin, rf_path, im_prefix='horizontally_translated_',
            im_path='../reconstructed_images/translated/')
    
    save_image(vert_translated_rf_bin, rf_path, im_prefix='vertically_translated_',
            im_path='../reconstructed_images/translated/')
    
    Image.fromarray(horz_translated_rf_bin * 255).show()
    Image.fromarray(vert_translated_rf_bin * 255).show()

    return 0

if __name__ == '__main__':
    main()

