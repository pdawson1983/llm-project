import os
from .get_files_info import get_files_info

def write_file(working_directory, file_path, content):
    file_info = get_files_info(working_directory, file_path)
    if file_info.startswith('Error:') and file_info.endswith("outside the allowed directory"):
        return file_info
    
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if file_info.endswith("does not exist in the allowed directory"):
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    try:
        with open(full_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
