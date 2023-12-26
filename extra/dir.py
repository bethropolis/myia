import os
 
# create directory if not exists
def create_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)