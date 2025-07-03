import os, subprocess
from .get_files_info import get_files_info

def run_python_file(working_directory, file_path):
    file_info = get_files_info(working_directory, file_path)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if file_info.startswith('Error:') and file_info.endswith("outside the allowed directory"):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if file_info.endswith("does not exist in the allowed directory"):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(['uv', 'run', file_path], cwd=working_directory ,timeout=30, capture_output=True, text=True)
        if result.returncode == 0:
            output = ""
            if result.stdout.strip():
                output += f"STDOUT:\n{result.stdout}"
            if result.stderr.strip():
                if output:
                    output += f"\nSTDERR:\n{result.stderr}"
                else:
                    output += result.stderr.strip()
            return f'Successfully executed "{file_path}":\n{output or "No output"}'
        else:
            return f'Error executing "{file_path}":\nSTDERR: {result.stderr}'
    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out after 30 seconds'
    except Exception as e:
        return f'Error: {e}'

