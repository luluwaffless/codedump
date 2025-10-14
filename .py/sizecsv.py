import os
import csv

def get_directory_size_and_file_count(directory):
    total_size = 0
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
                file_count += 1
    return total_size, file_count

def main(parent_directory, output_csv):
    directory_info = []
    for item in os.listdir(parent_directory):
        item_path = os.path.join(parent_directory, item)
        if os.path.isdir(item_path):
            size, file_count = get_directory_size_and_file_count(item_path)
            directory_info.append((item, size, file_count))
    
    # Sort the directories by size in descending order
    directory_info.sort(key=lambda x: x[1], reverse=True)
    
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Directory', 'Size (bytes)', 'File Count'])
        for directory, size, file_count in directory_info:
            csv_writer.writerow([directory, size, file_count])

if __name__ == "__main__":
    parent_directory = input('input path to dump info: ')
    output_csv = f'dir_sizes.csv'
    main(parent_directory, output_csv)