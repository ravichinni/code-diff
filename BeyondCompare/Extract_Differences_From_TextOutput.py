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

# Example usage
# file_path = r'D:\work\temp\text-report-statistics.txt'  # Replace 'path_to_your_file.txt' with the actual file path
# number = extract_number_from_last_line(file_path)
# print("Number at the beginning of the last line:", number)
