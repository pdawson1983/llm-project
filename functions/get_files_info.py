import os
from google.genai import types

def get_files_info(working_directory, directory=None):

    if directory is None:
        directory = '.'
        
    allowed_path = os.path.abspath(working_directory)
    requested_path = os.path.abspath(os.path.join(working_directory, directory))

    
    
    if not requested_path.startswith(allowed_path):
        return f'Error: cannot list "{directory}" as it is outside the allowed directory'
    
    if not os.path.exists(requested_path):
        return f'Error: "{directory}" does not exist in the allowed directory'
    
    if not os.path.isdir(requested_path):
        return f'Error: "{directory}" is not a directory'
    
    if directory == '.':
        display_directory = "current"
    else:
        display_directory = f"'{directory}'"
    
    file_info = f"Result for {display_directory} directory:\n"
    try:
        for item in os.listdir(requested_path):
            item_path = os.path.join(requested_path, item)
            file_info += f'\t- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}\n'
        return file_info
    except Exception as e:
        return f'Error: {e}'



