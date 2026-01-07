import os


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_dir_abs, target_file_abs]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        if os.path.dirname(target_file_abs):
            os.makedirs(os.path.dirname(target_file_abs), exist_ok=True)

        with open(target_file_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" {len(content)} characters written)'
    except OSError as e:
        return f"Error: {e}"
