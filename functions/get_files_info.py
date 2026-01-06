import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for entry in os.listdir(target_dir):
            path = os.path.join(target_dir, entry)
            lines.append(
                f"- {entry}: file_size={os.path.getsize(path)} bytes, "
                f"is_dir={os.path.isdir(path)}"
            )

        return "\n".join(lines)

    except OSError as e:
        return f"Error: {e}"
