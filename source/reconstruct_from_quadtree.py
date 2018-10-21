# Program to reconstruct a binary image from its corresponding quadtree representation
# Usage: python reconstruct_from_quadtree.py path_to_text_file_containing_quadtree_representation 
# Example: python reconstruct_from_quadtree.py ../quadtree_codes/im1_quadtree_codes.txt

import numpy as np
from PIL import Image
import os
import argparse

def is_leaf(code, quadtree):
    # Function to check whether a block is a leaf in the quadtree
    if (code in quadtree.keys()):
        # If the block with the given code is a leaf, then true(1) is
        # returned along with the color of the block(0/1)
        return (1, quadtree[code])
    else:
        # If the block is not a leaf false(0) is returned
        return (0, 0)

def recursive_reconstruction(im, quadtree, code):
    # Function to recursively reconstruct the image by obtaining colors
    # of the constituent leaf blocks from the quadtree
    leaf, color = is_leaf(code, quadtree)
    if (leaf):
        im[:, :] = 1 if color else 0
        return im
    n_rows, n_cols = im.shape[0], im.shape[1]
    # Recursively explore and reconstruct the 4 quadrants of the image
    recursive_reconstruction(im[:int(n_rows/2), :int(n_cols/2)], quadtree, (code + '0'))
    recursive_reconstruction(im[:int(n_rows/2), int(n_cols/2):], quadtree, (code + '1'))
    recursive_reconstruction(im[int(n_rows/2):, :int(n_cols/2)], quadtree, (code + '2'))
    recursive_reconstruction(im[int(n_rows/2):, int(n_cols/2):], quadtree, (code + '3'))
    return im

def quadtree_to_binary(quadtree):
    # Function to reconstruct a binary image from its given quadtree representation
    im_dims = quadtree['im_dims']
    # Initialize the image as a primitive block of all zeros
    reconstructed_im = np.zeros(im_dims)
    # Function call for recursively reconstructing the image
    recursive_reconstruction(reconstructed_im, quadtree, '0')
    return reconstructed_im

def parse_qt_code_file(qt_code_path):
    # Function to parse a file containing a quadtree representation of an image
    # and store the representation in a dictionary
    with open(qt_code_path, 'r') as f:
        qt_codes = f.readlines()
    im_dims = [int(i) for i in qt_codes[0][1:-2].split(', ')]
    qt_leaves = qt_codes[1:]
    quadtree = {}
    quadtree['im_dims'] = tuple(im_dims)
    for (i, l) in enumerate(qt_leaves):
        leaf = [str(i) for i in l[2:-2].split('\', ')]
        quadtree[leaf[0]] = int(leaf[1])
    return quadtree

def save_reconstructed_im(reconstructed_im, qt_code_path):
    # Function for saving an image reconstructed from its quadtree representation
    im_name = 'reconstructed_' + qt_code_path.split('/')[-1].split('.')[0].split('_')[0] + '_quadtree.png'
    im_path = '../reconstructed_images/quadtree/'
    if (not os.path.exists(im_path)):
        os.makedirs(im_path)
    Image.fromarray((reconstructed_im * 255)).convert('L').save((im_path + im_name), 'PNG')

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('qt_code_path', type=str)
    args = parser.parse_args()
    qt_code_path = args.qt_code_path
    # Function call for parsing the given quadtree file
    quadtree = parse_qt_code_file(qt_code_path)
    # Reconstruct the binary image from its given quadtree representation
    reconstructed_im = quadtree_to_binary(quadtree)
    # Save the reconstructed image
    save_reconstructed_im(reconstructed_im, qt_code_path)
    return 0

if __name__ == '__main__':
    main()

