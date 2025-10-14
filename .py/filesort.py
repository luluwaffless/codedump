import os
import shutil
def sort_files_by_type(directory):
    if not os.path.isdir(directory):
        print(f"The provided path '{directory}' is not a valid directory.")
        return
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            _, ext = os.path.splitext(filename)
            if not ext:
                ext = "no_extension"
            else:
                ext = ext.lower()
            target_folder = os.path.join(directory, ext)
            os.makedirs(target_folder, exist_ok=True)
            new_path = os.path.join(target_folder, filename)
            shutil.move(filepath, new_path)
            print(f"Moved '{filename}' → '{target_folder}/'")
    print("Sorting complete!")
if __name__ == "__main__":
    dir_path = input("Enter the path of the directory to sort: ").strip('"')
    sort_files_by_type(dir_path)