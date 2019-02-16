# Program to produce grayscale and binarized versions of a given set of input images
# Usage: python preprocess_images.py --dataset_path path_to_folder_containing_images --target_path path_to_target_folder
# Example: python preprocess_images.py --dataset_path ../test_images/original/ --target_path ../test_images/

from PIL import Image
import numpy as np
import cv2
import argparse
import os
import glob
import sys

def binarize_images(images, target_path, target_im_dims):
    # Function to binarize a given set of images
    sub_path = str(target_im_dims[0]) + 'x' + str(target_im_dims[1])
    target_path = target_path + 'binary/' + sub_path + '/'
   
    # Iterate over all images
    for image in images:
        # Obtain image name from image path based on the platform
        # on which the program is running
        if (sys.platform[:3] == 'win'):
            image_name = image.split('\\')[-1].split('.')[0]
        else:
            image_name = image.split('/')[-1].split('.')[0]

        # Set target image name
        image_name = image_name  + '_' + sub_path

        # If target folder does not exist, create it
        if (not os.path.exists(target_path)):
            os.makedirs(target_path)

        # Read, resize, binarize and save image in the target folder
        x = cv2.resize(np.array(Image.open(image).convert('L')), target_im_dims)
        x = x > np.mean(x)
        Image.fromarray((x * 255)).convert('L').save((target_path + image_name + '.png'), 'PNG')

def convert_to_grayscale(images, target_path, target_im_dims):
    # Function to convert a given set of images to grayscale
    sub_path = str(target_im_dims[0]) + 'x' + str(target_im_dims[1])
    target_path = target_path + 'grayscale/' + sub_path + '/'

    # Iterate over all images
    for image in images:
        # Obtain image name from image path based on the platform
        # on which the program is running
        if (sys.platform[:3] == 'win'):
            image_name = image.split('\\')[-1].split('.')[0]
        else:
            image_name = image.split('/')[-1].split('.')[0]
        
        # Set target image name
        image_name = image_name  + '_' + sub_path
        
        # If target folder does not exist, create it
        if (not os.path.exists(target_path)):
            os.makedirs(target_path)
        
        # Save the grayscale version of the image in the target folder
        Image.fromarray(cv2.resize(np.array(Image.open(image).convert('L')), 
            target_im_dims)).save((target_path + image_name + '.png'), 'PNG')

def read_images(path):
    # Function to read all images from a given path
    images = glob.glob(path + '/*.jpg') + glob.glob(path + '/*.png')
    return images


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', type=str)
    parser.add_argument('--target_path', type=str)
    args = parser.parse_args()

    # Get dataset and target folder path from command-line arguments
    dataset_path = args.dataset_path
    target_path = args.target_path

    # Read images from given path
    images = read_images(dataset_path)

    # Set dimensions of target images
    target_im_dims = (256, 256)

    # Convert all images to grayscale and save
    convert_to_grayscale(images, target_path, target_im_dims)

    # Convert all images to binary and save
    binarize_images(images, target_path, target_im_dims)

if __name__ == '__main__':
    main()

