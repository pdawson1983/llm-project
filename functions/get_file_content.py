import os


MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    allowed_path = os.path.abspath(working_directory)
    requested_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not requested_file_path.startswith(allowed_path):
        return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(requested_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        if len(open(requested_file_path, 'r').read()) > 10000:
            large_string = f'...File "{file_path}" truncated at 10000 characters'
        else:
            large_string = ''
        with open(requested_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        return file_content_string + f'\n{large_string}' 
    except Exception as e:
        return f'Error: {e}'

        