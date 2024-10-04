import os
import json

def find_json_with_id(start_dir, output_file):
    with open(output_file, 'w') as outfile:
        # Walk through all directories and files
        for root, dirs, files in os.walk(start_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        # Open and load the JSON file
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file)
                            
                            # Check if 'Id' key exists in the JSON data
                            # if 'Id' in data:
                            outfile.write(f"{file_path}\n")
                            # print(f"Found 'Id' in: {file_path}")
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {file_path}")
                    except Exception as e:
                        print(f"An error occurred with file {file_path}: {e}")

# Example usage
start_directory = './api_emulator/redfish/static'  # Replace with your starting directory
output_file_path = 'get_calls.txt'               # The file to write paths into
find_json_with_id(start_directory, output_file_path)
# print(output_file_path)
