import os
from config import FILE_READ_SIZE_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file_abs]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_abs, "r") as f:
            content = f.read(FILE_READ_SIZE_LIMIT)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {FILE_READ_SIZE_LIMIT} characters]'
        return content
    except OSError as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get content of the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="Get content of the file",
            ),
        },
    ),
)
