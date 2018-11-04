def parse_run_forest_file(rf_path):
    # Function to parse a file containing a run-forest representation

    # Open and read all lines from the file containing the run-forest representation
    with open(rf_path, 'r') as rf_file:
        rf_lines = rf_file.readlines()

    # Obtain image shape
    im_shape = tuple([int(i) for i in rf_lines[0][1:-2].split(', ')])
    
    # Obtain run-forest columns
    rf_cols = []
    for (i, line) in enumerate(rf_lines[1:]):
        col = []
        if(line != '[]\n'):
            line = line[2:-3].split('), (')
            for j in line:
                start, end = [int(k) for k in j.split(', ')]
                col.append((start, end))
        rf_cols.append(col)

    # Create a 2-tuple containing image-shape and a list containing
    # the run-forest columns
    run_forest = (im_shape, rf_cols)

    # Return the parsed run-forest
    return (run_forest)

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

