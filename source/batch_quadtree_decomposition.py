import os
import glob
import argparse
import sys
from quadtree_decomposition import *;

def batch_quadtree_decomposition(images):
    target_path = '../quadtree_codes/1024x1024/'
    for im in images:
        if (sys.platform[:3] == 'win'):
            image_name = im.split('\\')[-1].split('.')[0]
        else:
            image_name = im.split('/')[-1].split('.')[0]
        img = Image.open(im).convert('L') #.resize((256, 256), Image.ANTIALIAS)
        im_dims = (1024, 1024)
        leaves = convert_to_quadtree(img, im_dims=im_dims)
        save_quadtree_codes(image_name, leaves, im_dims, target_path)
 
def read_images(dataset_path):
    images = glob.glob(dataset_path + '/*.png')
    return images

def get_dataset_path_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_path', type=str)
    args = parser.parse_args()
    return args.dataset_path

def main():
    dataset_path = get_dataset_path_from_args()
    images = read_images(dataset_path)
    batch_quadtree_decomposition(images)

if __name__ == '__main__':
    main()

