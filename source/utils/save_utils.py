import os

def save_run_forest(rf, im_path, suffix='_run_forest', target_path='../run_forest_representations/'):
    # Function for saving the run-forest representation as a text-file

    # Get image name
    im_name = im_path.split('/')[-1].split('.')[0]

    # Create folder for saving run-forest representations if it
    # doesn't already exist
    if(not os.path.exists(target_path)):
            os.makedirs(target_path)

    # Set path for saving file
    file_name = target_path + im_name + suffix + '_.txt'

    # Open the file and write the run-forest representation
    with open(file_name, 'w') as rf_file:
        rf_file.write((str(rf[0]) + '\n'))
        for i in rf[1]:
            rf_file.write((str(i) + '\n'))
    return file_name

def save_quadtree_codes(im_path, quadtree, target_path='../quadtree_codes/'):
    # Save the quadtree representation of the given binary image
    im_dims, leaves = quadtree
    if (not os.path.exists(target_path)):
        os.makedirs(target_path)
    file_name = im_path.split('/')[-1].split('.')[0]
    code_file = target_path + file_name + '_quadtree_codes.txt'
    with open(code_file,'w') as f:
        f.write((str(im_dims) + '\n'))
        for leaf in leaves:
            f.write((str(leaf) + '\n'))
    return code_file

