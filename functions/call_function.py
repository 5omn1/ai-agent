from google.genai import types
from .get_files_info import *
from .get_file_content import *
from .run_python_file import *
from .write_file import *

available_functions = types.Tool(
    function_declarations=[schema_get_file_info,
                           schema_get_file_content,
                           schema_run_python_file,
                           schema_write_file],
)

def call_function(function_call, verbose=False):
    if not verbose:
        print(f"{function_call.name}")
    else:
        print(f"{function_call.name}({function_call.args})")

    function_name = function_call.name or ""
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in function_map.keys():
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
            )
        ]
    )
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    if "file" in args and "file_path" not in args:
        args["file_path"] = args.pop("file")

    function_result = function_map[function_name](**args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)



