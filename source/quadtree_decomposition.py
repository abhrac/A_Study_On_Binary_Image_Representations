# Program to decompose an image into its quadtree representation
# Usage: python quadtree_decomposition.py path_to_image
# Example: python quadtree_decomposition.py ../test_images/im1.jpg

from PIL import Image
import numpy as np
import cv2
import os
import argparse

def binarize(im):
    # Function for binarizing a given image
    return ((im > np.mean(im)) * 1)

def test_homogeneity(im):
    # Function for testing whether a given image is a 
    # homogeneous block (all pixels of same color)
    if (im[0, 0] == 1):
        return (np.sum(im) == (im.shape[0] * im.shape[1]))
    else:
        return (np.sum(1 - im) == (im.shape[0] * im.shape[1]))

def recursive_decomposition(im, code, leaves):
    # Function for recursively decomposing an image into homogeneous blocks
    # and generating corresponding codes for such blocks
    if (test_homogeneity(im)):
        # Stop recursion if the block is homogeneous and append
        # binary code for the block (black-0/white-1)
        leaves.append((code, im[0, 0]))
        return leaves
    n_rows, n_cols = im.shape[0], im.shape[1]
    # Recursively decompose the 4-quadrants
    leaves = recursive_decomposition(im[:int(n_rows/2), :int(n_cols/2)], (code + '0'), leaves) # quad-0
    leaves = recursive_decomposition(im[:int(n_rows/2), int(n_cols/2):], (code + '1'), leaves) # quad-1
    leaves = recursive_decomposition(im[int(n_rows/2):, :int(n_cols/2)], (code + '2'), leaves) # quad-2
    leaves = recursive_decomposition(im[int(n_rows/2):, int(n_cols/2):], (code + '3'), leaves) # quad-3
    return leaves

def convert_to_quadtree(im, im_dims=(256, 256)):
    # Function for converting a given binary image into its corresponding
    # quadtree representation
    im = cv2.resize(np.array(im), im_dims)
    bin_im = binarize(im)
    leaves = recursive_decomposition(bin_im, '0', [])
    return leaves

def save_quadtree_codes(im_path, leaves, im_dims):
    # Save the quadtree representation of the given binary image
    path = '../quadtree_codes/'
    if (not os.path.exists(path)):
        os.makedirs(path)
    file_name = im_path.split('/')[-1].split('.')[0]
    code_file = path + file_name + '_quadtree_codes.txt'
    with open(code_file,'w') as f:
        f.write((str(im_dims) + '\n'))
        for leaf in leaves:
            f.write((str(leaf) + '\n'))
    return 1

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('im_path', type=str)
    args = parser.parse_args()
    im_path = args.im_path
    # Open image from the given location
    im = Image.open(im_path).convert('L')
    # Specify image resize dimensions for computational simplifications
    im_dims = (256, 256)
    # Decompose the given image into its quadtree representation
    # and get the leaf codes for the corresponding quadtree
    leaves = convert_to_quadtree(im, im_dims=im_dims)
    # Save the quadtree leaf codes
    save_quadtree_codes(im_path, leaves, im_dims)
    return 0

if __name__ == '__main__':
    main()

