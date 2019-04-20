from PIL import Image
import numpy as np
import argparse

def zoom(im, factor):
    height, width = im.shape
    zoomed_im = np.zeros(((height*factor), (width*factor)))
    for i in range(0, height):
        for j in range(0, width):
            zoomed_im[(i*factor) : ((i+1)*factor), (j*factor) : ((j+1)*factor)] = im[i, j]
    return zoomed_im

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

    zoomed_im = zoom(bin_im, 4)
    
    Image.fromarray(bin_im * 255).show()
    Image.fromarray(zoomed_im * 255).show()

    return 0

if __name__ == '__main__':
    main()

