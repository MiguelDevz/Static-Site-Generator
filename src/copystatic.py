import os
import shutil

def copy_files_recursively(src_dir_path, dst_dir_path):
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)
    
    for filename in os.listdir(src_dir_path):
        #From ./static
        from_src = os.path.join(src_dir_path, filename)
        #To ./public
        to_dst = os.path.join(dst_dir_path, filename)
        if os.path.isfile(from_src):
            shutil.copy(from_src, to_dst)
            print(f" * {from_src} -> {to_dst}")
        else:
            copy_files_recursively(from_src, to_dst)