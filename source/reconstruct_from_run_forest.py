# Program to reconstruct a binary image from its corresponding run-forest representation
# Usage: python reconstruct_from_run_forest.py path_to_text_file_containing_run_forest_representation 
# Example: python reconstruct_from_run_forest.py ../run_forest_representations/im1_run_forest.txt

import numpy as np
from PIL import Image
import argparse
import os

def run_forest_to_binary(rf):
    # Function to reconstruct binary image from its run-forest representation

    # Get image shape from run-forest
    im_shape = rf[0]

    # Get list containing column runs from run-forest
    rf_cols = rf[1]

    # Initialize a matrix of all 0s of im_shape
    # This matrix will eventually become the reconstructed binary image
    bin_im = np.zeros(im_shape)

    # Iterate through all the column-lists in the run forest
    for (i, col) in enumerate(rf_cols):

        # The tuples in the column list contain start and end indices of runs in that column
        # For every tuple encountered, set all the elements between start-index and end-index 
        # (obatained from the tuple elements) in the ith column of the matrix bin_im to 1
        for run in col:
            bin_im[run[0]:run[1], i] = 1
    # Return the reconstructed binary image
    return bin_im

def parse_run_forest_file(rf_path):
    # Function to parse a file containing a run-forest representation

    # Open and read all lines from the file containing the run-forest representation
    with open(rf_path, 'r') as rf_file:
        rf_lines = rf_file.readlines()

    # Obtain image shape
    im_shape = tuple([int(i) for i in rf_lines[0][1:-2].split(', ')])
    
    # Obtain run-forest columns
    rf_cols = []
    for (i, line) in enumerate(rf_lines[1:]):
        col = []
        if(line != '[]\n'):
            line = line[2:-3].split('), (')
            for j in line:
                start, end = [int(k) for k in j.split(', ')]
                col.append((start, end))
        rf_cols.append(col)

    # Create a 2-tuple containing image-shape and a list containing
    # the run-forest columns
    run_forest = (im_shape, rf_cols)

    # Return the parsed run-forest
    return (run_forest)

def save_image(im, rf_path, im_prefix='', im_path='../reconstructed_images/run_forest/'):
    # Function for saving the reconstructed image
    im_name = im_prefix + rf_path.split('/')[-1].split('.')[0] 
    if (not os.path.exists(im_path)):
        os.makedirs(im_path)
    Image.fromarray(im * 255).convert('L').save((im_path + 'reconstructed_' + im_name + '.png'), "PNG")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("rf_path", type=str)
    args = parser.parse_args()

    # Get path containing run-forest file
    # from command-line argument
    rf_path = args.rf_path
    
    # Parse run-forest file
    rf = parse_run_forest_file(rf_path)

    # Reconstruct the binary image represented
    # by the run-forest
    bin_im = run_forest_to_binary(rf)

    # Display the reconstructed binary image
    Image.fromarray(bin_im * 255).show()

    # Save the reconstructed binary image
    save_image(bin_im, rf_path)
    return 0

if __name__ == '__main__':
    main()

