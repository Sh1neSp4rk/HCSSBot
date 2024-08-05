import os
import glob
import logging

def cleanup_files(folder_path):
    # Create a list of all files in the specified folder
    files = glob.glob(os.path.join(folder_path, '*'))
    
    # Iterate over the list of files and delete each one
    for file in files:
        try:
            os.remove(file)
            logging.info(f"Deleted: {file}")
        except Exception as e:
            logging.error(f"Error deleting {file}: {e}")

if __name__ == "__main__":
    folder_path = 'Files'  # Path to the folder you want to clean up
    cleanup_files(folder_path)
