# file_operations.py
import shutil
import os

def direct_copy_file(src_file_path, des_file_path):
    """Directly copy a file from the source path to the destination path using shutil."""
    # Ensure the destination directory exists, if not, create it
    des_dir = os.path.dirname(des_file_path)
    if not os.path.exists(des_dir):
        os.makedirs(des_dir)
        print(f"Destination directory {des_dir} created.")
   
    # Perform the file copy
    shutil.copy(src_file_path, des_file_path)
    print(f"Copied {src_file_path} to {des_file_path}")