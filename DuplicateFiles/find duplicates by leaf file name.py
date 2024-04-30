import os
import csv
from collections import defaultdict

def extract_leaf_filename(filename):
    # Split the filename by '#' characters and return the last part
    parts = filename.split("#")
    return parts[-1]

def find_duplicate_files(directory, output_csv):
    # Dictionary to store leaf filenames and their corresponding paths
    leaf_filename_dict = defaultdict(list)

    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        if "src" in dirs:
            src_path = os.path.join(root, "src")
            for _, _, src_files in os.walk(src_path):
                for file in src_files:
                    # Get the full path of the file
                    file_path = os.path.join(src_path, file)
                    # Extract only the filename
                    file_name = os.path.basename(file_path)
                    # Extract the leaf filename
                    leaf_filename = extract_leaf_filename(file_name)
                    # Append the file path to the list of paths for this leaf filename
                    leaf_filename_dict[leaf_filename].append(file_path)

    # Filter out leaf filenames that appear more than once
    duplicate_files = {leaf_filename: paths for leaf_filename, paths in leaf_filename_dict.items() if len(paths) > 1}

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Leaf Filename", "Count", "Paths"])
        for leaf_filename, paths in duplicate_files.items():
            csv_writer.writerow([leaf_filename, len(paths), ";".join(paths)])

# Example usage
directory_to_search = "D:\Work\SAP\ABB"
output_csv_file = "duplicate_files.csv"
find_duplicate_files(directory_to_search, output_csv_file)
