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

    module_beyond_compare_file_comparision.main_execute_bc_find_difference_count(
        r'@D:\Git-RaviChinni\code-diff\BeyondCompare\script.txt',
        r'D:\Work\temp\pwss#commercial_invoice_v2.ssfo.xml',
        r'D:\Work\temp-right\pweaver#commercial_invoice_v2.ssfo.xml',
        r'D:\work\temp\comparison_report.html',
        r'D:\work\temp\comparison_report_summary.txt')
#TODO: Delete temp file after use