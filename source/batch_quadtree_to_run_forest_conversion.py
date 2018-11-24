import argparse
import glob
import sys
from quadtree_to_run_forest import *;

def batch_quadtree_to_run_forest_conversion(quadtrees):
    target_path = '../run_forest_representations/from_quadtrees/'
    for qt in quadtrees:
        if (sys.platform[:3] == 'win'):
            qt_name = qt.split('\\')[-1].split('.')[0]
        else:
            qt_name = qt.split('/')[-1].split('.')[0]
        quadtree = parse_qt_code_file(qt)
        run_forest = quadtree_to_run_forest(quadtree)
        save_run_forest(run_forest, qt_name, target_path)

def get_dataset_path_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('quadtree_dataset_path', type=str)
    args = parser.parse_args()
    return args.quadtree_dataset_path

def read_from_path(dataset_path):
    quadtrees = glob.glob(dataset_path + '/*.txt')
    return quadtrees

def main():
    quadtree_dataset_path = get_dataset_path_from_args()
    quadtrees = read_from_path(quadtree_dataset_path)
    batch_quadtree_to_run_forest_conversion(quadtrees)

if __name__ == '__main__':
    main()

