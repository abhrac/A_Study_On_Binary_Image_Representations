from PIL import Image
import numpy as np
import argparse

def vertical_edge_structuring_element():
    struct_elm = (np.zeros((3, 3)), np.zeros((3, 3)))
    struct_elm[0][:, 1:] = 1
    struct_elm[1][:, :2] = 1
    return struct_elm

def horizontal_edge_structuring_element():
    struct_elm = (np.zeros((3, 3)), np.zeros((3, 3)))
    struct_elm[0][1:, :] = 1
    struct_elm[1][:2, :] = 1
    return struct_elm

def binarize(im):
    return ((im > np.mean(im)) * 1)

def aligns(region, struct_elm):
    for i in range(region.shape[0]):
        for j in range(region.shape[1]):
            if (struct_elm[i, j] != -1):
                if (region[i, j] != struct_elm[i, j]):
                    return False
    return True

def hit_or_miss(im, struct_elm):
    se_height, se_width = struct_elm.shape
    vert_range, horz_range = (im.shape[0]-se_height), (im.shape[1]-se_width)
    corners = np.zeros(im.shape)
    for i in range(vert_range):
        for j in range(horz_range):
            region = im[i:(i+se_height), j:(j+se_width)]
            center_x, center_y = se_height//2, se_width//2
            if (aligns(region, struct_elm)):
                corners[(i+center_x), (j+center_y)] = 1
    return corners

def show_image_edge_maps(vert_edges, horz_edges, edges):
    Image.fromarray(vert_edges * 255).show()
    Image.fromarray(horz_edges * 255).show()
    Image.fromarray(edges * 255).show()
    return 0

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('im_path', type=str)
    args = parser.parse_args()
    return args.im_path

def main():
    im_path = get_arguments()
    im = np.array(Image.open(im_path).convert('L'))
    bin_im = binarize(im)

    vert_struct_elm = vertical_edge_structuring_element()
    horz_struct_elm = horizontal_edge_structuring_element()

    left_edges = hit_or_miss(bin_im, vert_struct_elm[0])
    right_edges = hit_or_miss(bin_im, vert_struct_elm[1])

    top_edges = hit_or_miss(bin_im, horz_struct_elm[0])
    bottom_edges = hit_or_miss(bin_im, horz_struct_elm[1])

    vert_edges = left_edges + right_edges
    horz_edges = top_edges + bottom_edges

    edges = vert_edges + horz_edges

    Image.fromarray(im).show()
    show_image_edge_maps(vert_edges, horz_edges, edges)

    return 0

if __name__ == '__main__':
    main()

