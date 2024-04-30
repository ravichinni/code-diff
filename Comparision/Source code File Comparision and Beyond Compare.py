# Note: They key in the dictionaries is the file name. 
# This assumes that there are NO duplicate files across the directories in the entire source code
# Infact there are a couple - package.devc.xml, #pweaver#.nspc.xml, these can be ignored.

import os
import csv
import sys
sys.path.append(r'D:\Git-RaviChinni\code-diff\BeyondCompare')
import module_beyond_compare_file_comparision

def extract_leaf_filename(file_name):
    parts = file_name.split('#')
    return parts[-1] if parts else file_name

def compare_versions(left_path, right_path, output_file):
    # Dictionary to store file paths for both versions
    left_files = {}
    right_files = {}

    # Traverse left version directory and store file paths
    for root, dirs, files in os.walk(left_path):
        if "src" in dirs:
            src_path = os.path.join(root, "src")
            for _, _, src_files in os.walk(src_path):
                for file in src_files:
                    # Replace 'pwss' with 'pweaver' in the file name
                    file_name = file.replace('pwss', 'pweaver')
                    left_leaf_file_name = extract_leaf_filename(file_name)
                    left_files[file_name] = {'OriginalFileName': file, 'FilePath': os.path.join(src_path, file), 'LeafFileName': left_leaf_file_name}

    # Traverse right version directory and store file paths
    for root, dirs, files in os.walk(right_path):
        if "src" in dirs:
            src_path = os.path.join(root, "src")
            for _, _, src_files in os.walk(src_path):
                for file in src_files:
                    right_files[file] = {'OriginalFileName': file, 'FilePath': os.path.join(src_path, file), 'LeafFileName': extract_leaf_filename(file)}

    # Compare file paths and create CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['FileStatus', 'LeftFileName', 'RightFileName', 'LeftFilePath', 'RightFilePath', 'LeftNumberOfLines', 'RightNumberOfLines', 'LeftFileNamePWeaver', 'LeftLeafFileName', 'RightLeafFileName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Step 1: Find files in both sides and write to output
        for file, left_data in list(left_files.items()):
            if file in right_files:
                right_data = right_files.pop(file)
                writer.writerow({'FileStatus': 'Both', 'LeftFileName': left_data['OriginalFileName'], 'RightFileName': right_data['OriginalFileName'], 'LeftFilePath': left_data['FilePath'], 'RightFilePath': right_data['FilePath'], 'LeftNumberOfLines': get_num_lines(left_data['FilePath']), 'RightNumberOfLines': get_num_lines(right_data['FilePath']), 'LeftFileNamePWeaver': file, 'LeftLeafFileName': left_data['LeafFileName'], 'RightLeafFileName': right_data['LeafFileName']})
                left_files.pop(file)

        # Step 2: Find files in both sides by comparing the LeafFileName and write to output
        for file, left_data in list(left_files.items()):
            for right_file, right_data in list(right_files.items()):
                if left_data['LeafFileName'] == right_data['LeafFileName']:
                    writer.writerow({'FileStatus': 'Both', 'LeftFileName': left_data['OriginalFileName'], 'RightFileName': right_data['OriginalFileName'], 'LeftFilePath': left_data['FilePath'], 'RightFilePath': right_data['FilePath'], 'LeftNumberOfLines': get_num_lines(left_data['FilePath']), 'RightNumberOfLines': get_num_lines(right_data['FilePath']), 'LeftFileNamePWeaver': file, 'LeftLeafFileName': left_data['LeafFileName'], 'RightLeafFileName': right_data['LeafFileName']})
                    left_files.pop(file)
                    right_files.pop(right_file)

        # Step 3: Left only and right only
        for file, data in left_files.items():
            writer.writerow({'FileStatus': 'LeftOnly', 'LeftFileName': data['OriginalFileName'], 'RightFileName': '', 'LeftFilePath': data['FilePath'], 'RightFilePath': '', 'LeftNumberOfLines': get_num_lines(data['FilePath']), 'RightNumberOfLines': '', 'LeftFileNamePWeaver': file, 'LeftLeafFileName': data['LeafFileName'], 'RightLeafFileName': ''})

        for file, data in right_files.items():
            writer.writerow({'FileStatus': 'RightOnly', 'LeftFileName': '', 'RightFileName': data['OriginalFileName'], 'LeftFilePath': '', 'RightFilePath': data['FilePath'], 'LeftNumberOfLines': '', 'RightNumberOfLines': get_num_lines(data['FilePath']), 'LeftFileNamePWeaver': '', 'LeftLeafFileName': '', 'RightLeafFileName': data['LeafFileName']})


def get_num_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)
    
def find_differences_for_files_with_same_name(input_csv_file_path, output_csv_file):
    # Specify Beyond Compare directory
    bc_path = r'C:\Program Files\Beyond Compare 4'
    bc_script_path = r'@D:\Git-RaviChinni\code-diff\BeyondCompare\script.txt'
    bc_comparison_report_folder_path = r'D:\work\temp\comparision_report'
    
    # Add Beyond Compare directory to the PATH
    module_beyond_compare_file_comparision.add_bc_to_path(bc_path)

    try:
        with open(input_csv_file_path, newline='') as input_csvfile, open(output_csv_file, 'w', newline='') as outfile:
            reader = csv.DictReader(input_csvfile)
            writer = csv.writer(outfile)
            writer.writerow(['LeftFilePath', 'RightFilePath', 'DifferenceCount', 'ComparisonReportPath', 'ComparisonReportSummaryPath'])  # Write header

            for row in reader:
                if row['FileStatus'] == 'Both' and os.path.splitext(row['RightFileName'])[1] == '.abap':
                    left_file_path = row['LeftFilePath']
                    right_file_path = row['RightFilePath']
                    comparison_report_filename = row['RightFileName'] + 'comparison_report.html'
                    comparison_report_filepath = os.path.join(bc_comparison_report_folder_path, comparison_report_filename)
                    comparison_summary_report_filename = row['RightFileName'] + 'comparison_summary_report.txt' 
                    comparison_summary_report_filepath = os.path.join(bc_comparison_report_folder_path, 
                                                                      comparison_summary_report_filename)

                    difference_count = module_beyond_compare_file_comparision.main_execute_bc_find_difference_count(
                        bc_script_path,
                        left_file_path,
                        right_file_path,
                        comparison_report_filepath,
                        comparison_summary_report_filepath)
                    writer.writerow([left_file_path, right_file_path, difference_count,
                                     comparison_report_filepath, comparison_summary_report_filepath ])
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    left_version_path = r'D:\Work\SAP\ABB'
    right_version_path = r'D:\Work\SAP\BaseCode'
    output_csv_file = r'D:\work\temp\comparison_by_filename_output.csv'

    compare_versions(left_version_path, right_version_path, output_csv_file)

    diff_count_input_csv_file = output_csv_file
    diff_count_output_csv_file = r'D:\work\temp\diff_count_for_files_with_same_name.csv'
    find_differences_for_files_with_same_name(diff_count_input_csv_file,diff_count_output_csv_file)