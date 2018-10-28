# Program to convert the quadtree representation of an image to its corresponding run-forest
# Usage: python quadtree_to_run_forest.py path_to_text_file_containing_quadtree_codes
# Example: python quadtree_to_run_forest.py ../quadtree_codes/im1_quadtree_codes.txt

from reconstruct_from_run_forest import *;
from concatenate_run_forests import *;
import argparse

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

def is_leaf(code, quadtree):
    # Function to check whether a block is a leaf in the quadtree
    if (code in quadtree.keys()):
        # If the block with the given code is a leaf, then true(1) is
        # returned along with the color of the block(0/1)
        return (1, quadtree[code])
    else:
        # If the block is not a leaf false(0) is returned
        return (0, 0)

def leaf_rf_representation(block_dims, color):
    # Function to generate a run-forest representation of a quadtree leaf
    # If the leaf is black, a run-forest of empty lists is returned

    # The number of empty lists corresponds to the number of columns
    # in the leaf block
    if (not color):
        return (block_dims, [[] for i in range(block_dims[1])])
    
    # If the leaf is white a run-forest consisting of lists of runs
    # representing entire columns is returned
    rf_cols = [[(0, block_dims[0])] for i in range(block_dims[1])]
    return (block_dims, rf_cols)

def merge_rf_blocks(im_dims, quadtree, code):
    # Function to recursively construct the run-forest by merging the
    # run-forest representations of the corresponding quadtree blocks
    
    # Function call to check if a block is a leaf in the quadtree
    # If so, the color of the leaf is obtained
    leaf, color = is_leaf(code, quadtree)
    if (leaf):
        # If the block happens to be a leaf, the corresponding
        # run-forest representation of the block is returned
        return leaf_rf_representation(im_dims, color)

    # Obtain dimensions of the block
    im_dims = int(im_dims[0]/2), int(im_dims[1]/2)

    # Recursively obtain the run-forest representations of the 4 blocks
    rf0 = merge_rf_blocks(im_dims, quadtree, (code + '0'))
    rf1 = merge_rf_blocks(im_dims, quadtree, (code + '1'))
    rf2 = merge_rf_blocks(im_dims, quadtree, (code + '2'))
    rf3 = merge_rf_blocks(im_dims, quadtree, (code + '3'))

    # Concatenate the 2 upper and 2 lower blocks horizontally to obtain
    # the respective upper and lower halves of the image
    rf_upper_half = horizontally_concatenate_run_forests(rf0, rf1)
    rf_lower_half = horizontally_concatenate_run_forests(rf2, rf3)

    # Vertically concatenate the upper and lower halves of the image to obtain
    # the full image and return the same
    return vertically_concatenate_run_forests(rf_upper_half, rf_lower_half)

def quadtree_to_run_forest(quadtree):
    # Function to convert a quadtree to its corresponding run-forest

    # Obtain image dimensions from the quadtree representation
    im_dims = quadtree['im_dims']

    # Function call to recursively construct the run-forest by merging the
    # run-forest representations of the corresponding quadtree blocks
    run_forest = merge_rf_blocks(im_dims, quadtree, '0')
    
    # Return the constructed run-forest
    return run_forest

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('quadtree_path', type=str)
    args = parser.parse_args()
    qt_path = args.quadtree_path
    
    # Obtain quadtree codes from the given file and parse the same
    quadtree = parse_qt_code_file(qt_path)

    # Obtain run-forest representation of the given quadtree
    run_forest = quadtree_to_run_forest(quadtree)

    # Reconstruct the image from the obtained run-forest (for verification)
    bin_im = run_forest_to_binary(run_forest)

    # Display the image reconstructed from the run-forest representation of
    # the given quadtree
    Image.fromarray(bin_im * 255).show()

    # Save the image reconstructed from the run-forest representation of
    # the given quadtree
    save_image(bin_im, qt_path, im_prefix='quadtree_to_run_forest_', 
            im_path='../reconstructed_images/quadtree_to_run_forest/')

if __name__ == '__main__':
    main()

