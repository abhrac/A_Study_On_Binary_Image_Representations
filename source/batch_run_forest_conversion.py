import os
import glob
import argparse
import sys
from get_run_forest_representation import *;

def batch_run_forest_conversion(images):
    target_path = '../run_forest_representations/256x256/'
    for im in images:
        if (sys.platform[:3] == 'win'):
            image_name = im.split('\\')[-1].split('.')[0]
        else:
            image_name = im.split('/')[-1].split('.')[0]
        img = Image.open(im).convert('L') #.resize((256, 256), Image.ANTIALIAS)
        img = binarize_image(img)
        run_forest = convert_to_run_forest(img)
        save_run_forest(run_forest, image_name, target_path)
 
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
    batch_run_forest_conversion(images)

if __name__ == '__main__':
    main()

