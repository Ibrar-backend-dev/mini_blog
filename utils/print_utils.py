import inspect
import json

from typing import Any


def color_print(text: str | Exception, color: str = "OKGREEN"):
    """Print text in color
    HEADER: purple
    OKBLUE: blue
    OKCYAN: cyan
    OKGREEN: green
    WARNING: yellow
    FAIL: red
    BOLD: bold
    UNDERLINE: underline
    """

    class bcolors:
        HEADER = "\033[95m"
        OKBLUE = "\033[94m"
        OKCYAN = "\033[96m"
        OKGREEN = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"

    if color == "green":
        print(f"{bcolors.OKGREEN}{text}{bcolors.ENDC}")

    elif color == "red":
        print(f"{bcolors.FAIL}{text}{bcolors.ENDC}")

    elif color == "blue":
        print(f"{bcolors.OKBLUE}{text}{bcolors.ENDC}")

    elif color == "yellow":
        print(f"{bcolors.WARNING}{text}{bcolors.ENDC}")

    elif color == "cyan":
        print(f"{bcolors.OKCYAN}{text}{bcolors.ENDC}")

    elif color == "purple":
        print(f"{bcolors.HEADER}{text}{bcolors.ENDC}")

    else:
        print(f"{getattr(bcolors, color.upper())}{text}{bcolors.ENDC}")


def print_test_header(test_name):
    color_print(
        f"""\n
        ----------------------------------------------------------------------------
                                    test: {test_name}
        ----------------------------------------------------------------------------
            """,
        "OKCYAN",
    )
    color_print("## =>  started", "WARNING")


def print_test_passed():
    color_print("## =>  passed", "OKGREEN")


def print_test_failed():
    color_print("## =>  failed", "FAIL")


def debug_print(data: dict[str, Any] | list[Any] | dict[int, Any], color: str = "green") -> None:
    frame = inspect.currentframe()
    try:
        var_name = [var_name for var_name, var_val in frame.f_back.f_locals.items() if var_val is data][0]  # type: ignore
    except Exception:
        var_name = "data"

    if color == "green":
        color_print(f"{var_name} = {jsonify(data)}", "OKGREEN")
    if color == "red":
        color_print(f"{var_name} = {jsonify(data)}", "FAIL")
    if color == "blue":
        color_print(f"{var_name} = {jsonify(data)}", "OKBLUE")
    if color == "yellow":
        color_print(f"{var_name} = {jsonify(data)}", "WARNING")
    if color == "cyan":
        color_print(f"{var_name} = {jsonify(data)}", "OKCYAN")
    if color == "purple":
        color_print(f"{var_name} = {jsonify(data)}", "HEADER")


def jsonify(data: dict[str, Any] | list[Any] | dict[int, Any]) -> str:
    return json.dumps(data, indent=4, default=str)


def error_message_detail(error):
    error_structure = getattr(error, "detail", str(error))

    error_message = ""
    if isinstance(error_structure, dict):
        errors = []
        for key, value in error_structure.items():
            custom_error_message = ""
            if isinstance(value, list):
                if key == "non_field_errors":
                    custom_error_message = value[0]
                else:
                    custom_error_message = f"{key}: {value[0]}"
                errors.append(custom_error_message)
            else:
                errors.append(str(value))
        error_message = ", ".join(errors)
    else:
        error_message = str(error_structure)

    return error_message
