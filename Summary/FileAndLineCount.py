import os
import glob
import csv

def count_lines(file_path):
    """Count the number of lines in a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)

def count_abap_files_and_lines(root_folder):
    """Count the number of ABAP files and lines of code in each src folder."""
    results = []
    
    for folder_name, _, _ in os.walk(root_folder):
        if os.path.basename(folder_name) == 'src':
            abap_files = glob.glob(os.path.join(folder_name, '*.abap'))
            total_lines = sum(count_lines(file_path) for file_path in abap_files)
            results.append((folder_name, len(abap_files), total_lines))

    return results

def save_to_csv(data, csv_file):
    """Save data to a CSV file."""
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Src Folder Path', 'Count of ABAP files', 'Sum of lines of code'])
        writer.writerows(data)

if __name__ == "__main__":
    root_folder = input("Enter the root folder path: ")
    csv_file = input("Enter the output CSV file path: ")

    results = count_abap_files_and_lines(root_folder)
    save_to_csv(results, csv_file)
    print("CSV file generated successfully.")
