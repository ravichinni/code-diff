import os
from collections import Counter

def find_duplicate_files(directory):
    # Dictionary to store filenames and their corresponding paths
    file_dict = Counter()

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
                    # Increment the count for this filename
                    file_dict[file_name] += 1

    # Filter out filenames that appear more than once
    duplicate_files = {filename: count for filename, count in file_dict.items() if count > 1}

    # Print the results
    for filename, count in duplicate_files.items():
        paths = []
        for root, dirs, files in os.walk(directory):
            if "src" in dirs:
                src_path = os.path.join(root, "src")
                for _, _, src_files in os.walk(src_path):
                    for file in src_files:
                        file_path = os.path.join(src_path, file)
                        if os.path.basename(file_path) == filename:
                            paths.append(file_path)
        print(f"Filename: {filename}")
        print(f"Count: {count}")
        print("Paths: " + ";".join(paths))
        print()

# Example usage
directory_to_search = "D:\Work\SAP\BaseCode"
find_duplicate_files(directory_to_search)
