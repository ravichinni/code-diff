# Setup instructions:
# To Run:
#   Install PowerShell 7
#   Install Beyond Compare 4
#   Install Python
# For Development: 
#   Install VS Code
#   Install VS Code extensions for Python, PowerShell 7 

import os
import tempfile
import shutil
import re

def add_bc_to_path(bc_path):
    """
    Add Beyond Compare directory to the PATH environment variable.
    """
    current_path = os.environ.get('PATH', '')
    if bc_path not in current_path:
        os.environ['PATH'] = f"{current_path};{bc_path}"
        print("Beyond Compare directory added to PATH.")
    else:
        print("Beyond Compare directory is already in PATH.")

def replace_string_in_file(file_path, old_string, new_string):
    """
    Replace old_string with new_string in the specified file.
    Match is case-sensitive and whole word only.
    Save the updated content to a temporary file.
    """
    # Create a temporary file to save the updated content
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        with open(file_path, 'r') as file:
            for line in file:
                # Construct regular expression pattern with word boundaries
                pattern = r"\b" + re.escape(old_string) + r"\b"
                # Use re.sub to perform the replacement
                updated_line = re.sub(pattern, new_string, line)
                temp_file.write(updated_line)

    # Get the path of the temporary file
    temp_file_path = temp_file.name

    print(f"String '{old_string}' replaced with '{new_string}'. Temporary file created at: {temp_file_path}")
    return temp_file_path


def run_bc_comparison(script_path, file1_path, file2_path, report_path, summary_report_path):
    """
    Call Beyond Compare to perform the comparison between two files.
    """
    os.system(f'BCompare.exe "{script_path}" "{file1_path}" "{file2_path}" "{report_path}" "{summary_report_path}"')

def extract_number_from_last_line(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            last_line = lines[-1].strip()
            number_at_beginning = ''
            for char in last_line:
                if char.isdigit():
                    number_at_beginning += char
                else:
                    break
            return int(number_at_beginning)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Specify Beyond Compare directory
    bc_path = r'C:\Program Files\Beyond Compare 4'
    
    # Add Beyond Compare directory to the PATH
    add_bc_to_path(bc_path)
    
    # Replace "PWSS" with "PWEAVER" in File 1
    file1_path = r'D:\Work\temp\pwss#commercial_invoice_v2.ssfo.xml'
    temp_file_path = replace_string_in_file(file1_path, 'PWSS', 'PWEAVER')
    
    # Call Beyond Compare to perform the comparison
    file2_path = r'D:\Work\temp-right\pweaver#commercial_invoice_v2.ssfo.xml'

    # Note: @ character at the start of the script path is needed for BC
    bcompare_script_path = r'@D:\Git-RaviChinni\code-diff\BeyondCompare\script.txt'
    comparison_report_path = r'D:\work\temp\comparison_report.html'
    comparison_summary_report_path = r'D:\work\temp\comparison_report_summary.txt'

    run_bc_comparison(bcompare_script_path, temp_file_path, file2_path, comparison_report_path, comparison_summary_report_path)
    difference_count = extract_number_from_last_line(comparison_summary_report_path)
    print("Number at the beginning of the last line:", difference_count)
#TODO: Delete temp file after use