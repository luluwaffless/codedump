import os
import datetime

def rename_files_by_modified_date(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files_with_mtime = []
    for f in files:
        path = os.path.join(folder_path, f)
        ctime = os.path.getctime(path)
        mtime = os.path.getmtime(path)
        print(f"{f}: created {datetime.datetime.fromtimestamp(ctime)}, modified {datetime.datetime.fromtimestamp(mtime)}")
        files_with_mtime.append((f, mtime))
    files_sorted = sorted(files_with_mtime, key=lambda x: x[1])
    for idx, (filename, _) in enumerate(files_sorted, start=1):
        name, ext = os.path.splitext(filename)
        new_name = f"{idx:03d}{ext}"
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name)
        if src != dst:
            os.rename(src, dst)
            print(f"Renamed: {filename} -> {new_name}")

rename_files_by_modified_date("jason")