import os
import shutil
def file(directory):
    for filename in os.listdir(directory):
        if filename != "desktop.ini":
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                continue
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension:
                folder_name = file_extension
            else:
                folder_name = "."
            target_directory = os.path.join(directory, folder_name)
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)
            shutil.move(file_path, os.path.join(target_directory, filename))
            print(f"Moved {filename} to {target_directory}")
file(input("insert directory to organize: "))