# Program to concatenate two images based on their run-forest representations
# Usage: python concatenate_run_forests.py path_to_image_1 path_to_image_2
# Example: python concatenate_run_forests.py ../test_images/im1.jpg ../test_images/im2.jpg

from get_run_forest_representation import *
from reconstruct_from_run_forest import *;
from PIL import Image
import cv2
import argparse

def horizontally_concatenate_run_forests(rf1, rf2):
    # Function for horizontally concatenating 2 run-forests
    
    # Obtain dimensions of the two images
    im1_dims, im2_dims = rf1[0], rf2[0]

    # If the number of rows in the images are different, throw an exception
    if (im1_dims[0] != im2_dims[0]):
        raise Exception("Image dimension mis-match. Number of rows must be same in both images.")
    # Obtain the dimensions of the concatenated image
    concat_dims = im1_dims[0], (im1_dims[1] + im2_dims[1])

    # Obtain the lists containing the columns of the two run-forests
    rf1_cols, rf2_cols = rf1[1], rf2[1]

    # Horizontally concatenate the columns of the two run-forests
    rf_cols = rf1_cols + rf2_cols

    # Return the horizontally concatenated run-forest
    return (concat_dims, rf_cols)

def increment_column_indices(col, l):
    # Function to increment the indices of the column runs by a certain constant
    for (i, run) in enumerate(col):
        col[i] = (run[0] + l), (run[1] + l)
    return col

def continuous_ends(col1, col2, l):
    # Function to check if the last run of col1 and the first run of col2
    # are contiguous, if, col1 is stacked on top of col2
    if ((col1[-1][1] == l) and (col2[0][0] == l)):
        return True
    return False

def merge_columns(col1, col2, l):
    # Function to merge two columns into one by stacking col1 on top of col2

    # Increment indices of col2 by the height of the image that col1 comes
    # from, as after stacking, runs in col2 will be a continuation of the
    # runs in col1
    col2 = increment_column_indices(col2, l)

    # If either of the columns is null, directly concatenate the two and return
    if ((col1 == []) or (col2 == [])):
        return (col1 + col2)
    
    # If the columns have continuous ends, define a junction run between
    # the two columns and then concatenate the two keeping the junction
    # in between
    if (continuous_ends(col1, col2, l)):
        junction = col1[-1][0], col2[0][1]
        col = col1[:-1] + [junction] + col2[1:]
        return col
    
    # If none of the above are true, simply return by concatenating the two
    return (col1 + col2)

def vertically_concatenate_run_forests(rf1, rf2):
    # Function for vertically concatenating 2 run-forests
    
    # Obtain the dimensions of the 2 images
    im1_dims, im2_dims = rf1[0], rf2[0]

    # If the number of columns in the images are different, throw an exception
    if (im1_dims[1] != im2_dims[1]):
        raise Exception("Image dimension mis-match. Number of columns must be same in both images.")
    # Obtain the dimensions of the concatenated image
    concat_dims = (im1_dims[0] + im2_dims[0]), im1_dims[1]

    # Obtain the lists containing the columns of the 2 run-forests
    rf1_cols, rf2_cols = rf1[1], rf2[1]

    # Initialize an empty list for storing the list of runs of the
    # concatenated image
    rf_cols = []

    # Iterate through the columns of the two images and concatenate them
    for i in range(concat_dims[1]):
        rf_cols.append(merge_columns(rf1_cols[i], rf2_cols[i], im1_dims[0]))
    
    # Return the run-forest representation of the concatenated image
    return (concat_dims, rf_cols)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('image_1', type=str)
    parser.add_argument('image_2', type=str)
    args = parser.parse_args()

    # Binarize given images
    im1 = binarize_image(cv2.resize(np.array(Image.open(args.image_1).convert('L')), (256, 256)))
    im2 = binarize_image(cv2.resize(np.array(Image.open(args.image_2).convert('L')), (256, 256)))
    
    # Obtain run-forest representations of two images
    rf1, rf2 = convert_to_run_forest(im1), convert_to_run_forest(im2)

    # Horizontally concatenate the run-forests of the 2 given images
    horz_concat_rf = horizontally_concatenate_run_forests(rf1, rf2)

    # Convert the horizontally concatenated images to binary
    horz_concat_bin = run_forest_to_binary(horz_concat_rf)

    # Vertically concatenate the 2 given images
    vert_concat_rf = vertically_concatenate_run_forests(rf1, rf2)

    # Convert the vertically concatenated image to binary
    vert_concat_bin = run_forest_to_binary(vert_concat_rf)
    
    # Save concatenated images
    save_image(horz_concat_bin, args.image_1, im_prefix='horizontal_rf_concat_', im_path='../reconstructed_images/run_forest/concatenated_images/')
    save_image(vert_concat_bin, args.image_1, im_prefix='vertical_rf_concat_', im_path='../reconstructed_images/run_forest/concatenated_images/')

    # Display concatenated images
    Image.fromarray(horz_concat_bin * 255).show()
    Image.fromarray(vert_concat_bin * 255).show()

if __name__ == '__main__':
    main()

