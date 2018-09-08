# Program to get the run-forest representation of an input image.
# Usage: python get_run_forest_representation.py path-to-input-image
# Example: python get_run_forest_representation.py ./test/im1.jpg
# Note: In this impementation, runs of 1s have been considered.

import numpy as np
from PIL import Image
import argparse
import os

def binarize_image(x):
    # Function for binarizing an input image

    # Convert image to a numpy array
    x = np.array(x)

    # Threshold pixel values: Set pixels below the mean of the
    # entire image to 0, set the rest to 1
    x = (x > np.mean(x))

    # Uncomment the next line to display the binary image
    #Image.fromarray(x * 255).show()

    # Return the binarized image
    return x

def get_end_index(col, pos):
    # Function for getting the end-index for the run
    # of 1s starting at pos

    # Loop until either a zero is encountered or the
    # entire column has been traversed
    while((pos < col.shape[0]) and (col[pos] != 0)):
        pos = pos + 1
    
    # Return the position of the end-index
    return pos

def column_list(col):
    # Function for converting a given column in the
    # image to its corresponding run-forest list
    
    # Initialize variable for keeping track of the traversal
    pos = 0

    # Initialize list for storing runs
    col_ls = []

    # Loop down the column
    while(pos < len(col)):

        # If a 1 is found, look for a run of 1s
        if(col[pos] == 1):

            # Store starting position of the run
            start_idx = pos

            # Function call for getting the end index
            # of the run
            end_idx = get_end_index(col, pos)

            # Append tuple containing start and end-index
            # of the run to the run-forest list
            col_ls.append((start_idx, end_idx))

            # Set value of tracking variable to the
            # end-index of the run
            pos = end_idx

        # Increment the tracking variable by 1 to
        # point to the next pixel in the column
        pos = pos + 1

    # Return the run-forest list corresponding to the
    # given image column
    return (col_ls)

def convert_to_run_forest(x):
    # Function to convert an input binary image to
    # its run-forest representation

    # Initialize list for storing run-forest columns
    rf_columns = []

    # Loop through all columns in the image
    for i in range(x.shape[1]):

        # Get ith image column
        col = x[:, i]

        # Get run-forest representation for ith column
        # and append a tuple containing index of the
        # ith column and the run-forest list
        rf_columns.append((i, column_list(col)))

    # Get the final run-forest by creating a tuple containing
    # the image-dimensions and the list of run-forest columns
    run_forest = x.shape, rf_columns

    # Return the final run-forest representation
    return (run_forest)

def save_run_forest(rf, im_path):
    # Function for saving the run-forest representation as a text-file

    # Get image name
    im_name = im_path.split('/')[-1].split('.')[0]

    # Create folder for saving run-forest representations if it
    # doesn't already exist
    if(not os.path.exists('../run_forest_representations/')):
            os.makedirs('../run_forest_representations/')

    # Set path for saving file
    file_name = '../run_forest_representations/' + im_name + '_run_forest.txt'

    # Open the file and write the run-forest representation
    with open(file_name, 'a') as rf_file:
        rf_file.write((str(rf[0]) + '\n'))
        for i in rf[1]:
            rf_file.write((str(i) + '\n'))

def main():
    # Parse command-line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('im_path', type=str)
    args = parser.parse_args()
    # Get image-path from parsed command-line argument
    im_path = args.im_path
    # Open image from the given path and convert image to grayscale
    img = Image.open(im_path).convert('L') #.resize((256, 256), Image.ANTIALIAS)
    # Binarize input image
    img = binarize_image(img)
    # Convert binarized image to corresponding run-forest representation
    run_forest = convert_to_run_forest(img)
    # Save the run-forest representation as a text-file
    save_run_forest(run_forest, im_path)
    return 0

if __name__ == '__main__':
    main()

