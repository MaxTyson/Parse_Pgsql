import os

def make_dir(name):
    # create directory calls results
    try:
        os.makedirs(name)
    except FileExistsError:
        pass