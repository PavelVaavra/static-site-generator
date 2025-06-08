import os
import shutil

def cp_dir(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    else:
        os.mkdir(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        if os.path.isfile(src_path):
            if not os.path.exists(dst):
                os.mkdir(dst)
            print(f"cp {src_path} to {dst}")
            shutil.copy(src_path, dst)
        else:
            cp_dir(os.path.join(src, item), os.path.join(dst, item))