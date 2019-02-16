import argparse
import glob
import sys
from run_forest_to_quadtree import *;

def batch_run_forest_to_quadtree_conversion(run_forests):
    for rf in run_forests:
        if (sys.platform[:3] == 'win'):
            rf_name = rf.split('\\')[-1].split('.')[0]
        else:
            rf_name = rf.split('/')[-1].split('.')[0]
        run_forest = parse_run_forest_file(rf)
        quadtree = run_forest_to_quadtree(run_forest)
        save_quadtree_from_rf(rf_name, quadtree)

def get_dataset_path_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('run_forest_dataset_path', type=str)
    args = parser.parse_args()
    return args.run_forest_dataset_path

def read_from_path(dataset_path):
    run_forests = glob.glob(dataset_path + '/*.txt')
    return run_forests

def main():
    run_forest_dataset_path = get_dataset_path_from_args()
    run_forests = read_from_path(run_forest_dataset_path)
    batch_run_forest_to_quadtree_conversion(run_forests)

if __name__ == '__main__':
    main()

