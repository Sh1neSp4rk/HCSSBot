# Tools/cleanup_files.py
import os
import glob
import logging

def cleanup_files(folder_path):
    files = glob.glob(os.path.join(folder_path, '*'))
    
    for file in files:
        try:
            os.remove(file)
            logging.info(f"Deleted: {file}")
        except Exception as e:
            logging.error(f"Error deleting {file}: {e}")

if __name__ == "__main__":
    folder_path = 'Files'
    cleanup_files(folder_path)
