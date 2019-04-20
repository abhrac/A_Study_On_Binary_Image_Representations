from PIL import Image
import numpy as np
import argparse

def get_subsample_value(block):
    return (np.sum(block) >= (block.shape[0] * block.shape[1]))

def subsample(im, factor):
    height, width = im.shape
    subsampled_im = np.zeros(((height//factor), (width//factor)))
    for i in range(0, height, factor):
        for j in range(0, width, factor):
            block = im[i:(i+factor), j:(j+factor)]
            subsampled_im[(i//factor), (j//factor)] = get_subsample_value(block)
    return subsampled_im

def binarize(im):
    return (im > np.mean(im))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('im_path', type=str)
    args = parser.parse_args()
    return args.im_path

def main():
    im_path = get_args()
    im = np.array(Image.open(im_path))
    bin_im = binarize(im)

    subsampled_im = subsample(bin_im, 4)
    
    Image.fromarray(bin_im * 255).show()
    Image.fromarray(subsampled_im * 255).show()

if __name__ == '__main__':
    main()

