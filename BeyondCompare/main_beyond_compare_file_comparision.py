# Setup instructions:
# To Run:
#   Install PowerShell 7
#   Install Beyond Compare 4
#   Install Python
# For Development: 
#   Install VS Code
#   Install VS Code extensions for Python, PowerShell 7 

# Usage:
# 

import module_beyond_compare_file_comparision

if __name__ == "__main__":
    # Specify Beyond Compare directory
    bc_path = r'C:\Program Files\Beyond Compare 4'
    
    # Add Beyond Compare directory to the PATH
    module_beyond_compare_file_comparision.add_bc_to_path(bc_path)
    
    # Replace "PWSS" with "PWEAVER" in File 1
    file1_path = r'D:\Work\temp\pwss#commercial_invoice_v2.ssfo.xml'
    temp_file_path = module_beyond_compare_file_comparision.replace_string_in_file(file1_path, 'PWSS', 'PWEAVER')
    
    # Call Beyond Compare to perform the comparison
    file2_path = r'D:\Work\temp-right\pweaver#commercial_invoice_v2.ssfo.xml'

    # Note: @ character at the start of the script path is needed for BC
    bcompare_script_path = r'@D:\Git-RaviChinni\code-diff\BeyondCompare\script.txt'
    comparison_report_path = r'D:\work\temp\comparison_report.html'
    comparison_summary_report_path = r'D:\work\temp\comparison_report_summary.txt'

    module_beyond_compare_file_comparision.run_bc_comparison(bcompare_script_path, temp_file_path, file2_path, comparison_report_path, comparison_summary_report_path)
    difference_count = module_beyond_compare_file_comparision.extract_number_from_last_line(comparison_summary_report_path)
    print("Number at the beginning of the last line:", difference_count)
#TODO: Delete temp file after use