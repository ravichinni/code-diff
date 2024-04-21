# Note: They key in the dictionaries is the file name. 
# This assumes that there are NO duplicate files across the directories in the entire source code
# Infact there are a couple - package.devc.xml, #pweaver#.nspc.xml, these can be ignored.

import os
import csv

def compare_versions(left_path, right_path, output_file):
    # Dictionary to store file paths for both versions
    left_files = {}
    right_files = {}

    # Traverse left version directory and store file paths
    for root, dirs, files in os.walk(left_path):
        if "src" in dirs:
            src_path = os.path.join(root, "src")
            for dirpath, _, src_files in os.walk(src_path):
                for file in src_files:
                    relative_path = os.path.relpath(dirpath, src_path)
                    file_name = file.replace('pwss', 'pweaver')
                    key = os.path.join(relative_path, file_name)
                    left_files[key] = {'OriginalFileName': file, 'FilePath': os.path.join(dirpath, file)}

    # Traverse right version directory and store file paths
    for root, dirs, files in os.walk(right_path):
        if "src" in dirs:
            src_path = os.path.join(root, "src")
            for dirpath, _, src_files in os.walk(src_path):
                for file in src_files:
                    relative_path = os.path.relpath(dirpath, src_path)
                    key = os.path.join(relative_path, file)
                    right_files[key] = {'OriginalFileName': file, 'FilePath': os.path.join(dirpath, file)}

    # Compare file paths and create CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['FileStatus', 'LeftFileName', 'RightFileName', 'LeftFilePath', 'RightFilePath', 'LeftNumberOfLines', 'RightNumberOfLines', 'LeftFileNamePWeaver']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Check files present only in the left version
        for key, data in left_files.items():
            if key not in right_files:
                writer.writerow({'FileStatus': 'LeftOnly', 'LeftFileName': data['OriginalFileName'], 'RightFileName': '', 'LeftFilePath': data['FilePath'], 'RightFilePath': '', 'LeftNumberOfLines': get_num_lines(data['FilePath']), 'RightNumberOfLines': '', 'LeftFileNamePWeaver': key})

        # Check files present only in the right version
        for key, data in right_files.items():
            if key not in left_files:
                writer.writerow({'FileStatus': 'RightOnly', 'LeftFileName': '', 'RightFileName': data['OriginalFileName'], 'LeftFilePath': '', 'RightFilePath': data['FilePath'], 'LeftNumberOfLines': '', 'RightNumberOfLines': get_num_lines(data['FilePath']), 'LeftFileNamePWeaver': ''})

        # Check files present in both versions
        for key, left_data in left_files.items():
            if key in right_files:
                right_data = right_files[key]
                writer.writerow({'FileStatus': 'Both', 'LeftFileName': left_data['OriginalFileName'], 'RightFileName': right_data['OriginalFileName'], 'LeftFilePath': left_data['FilePath'], 'RightFilePath': right_data['FilePath'], 'LeftNumberOfLines': get_num_lines(left_data['FilePath']), 'RightNumberOfLines': get_num_lines(right_data['FilePath']), 'LeftFileNamePWeaver': key})


def get_num_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)


# Example usage:
left_version_path = 'D:\Work\SAP\ABB'
right_version_path = 'D:\Work\SAP\BaseCode'
output_csv_file = 'comparison_output.csv'

compare_versions(left_version_path, right_version_path, output_csv_file)
