import os
import ast

import hashlib


def type_python_to_intermediate(python_hint):
    return {
        "int": "number",
        "str": "String"
    }[python_hint]


def type_intermediate_to_dvm(t):
    return {
        "int": "Uint64",
        "number": "Uint64",
        "str": "String",
        "String": "String"
    }[t]


def flatten_list(lists):
    output = []
    for i in lists:
        if isinstance(i, list):
            output.extend(flatten_list(i))
        else:
            output.append(i)

    return output


def filter_args_out(args):
    if isinstance(args, ast.arg):
        if args.arg == 'self':
            return False
    return True


def print_interpreter(msg: list):
    try:
        term_width = os.get_terminal_size().columns
    except OSError:
        term_width = 80

    def format_column(content, width):
        if len(content) > width:
            content = content[:width-3] + "..."
        else:
            content = content + " " * (width - len(content))
        return content
    
    # split the terminal into three columns, 50%, 25%, 25%
    widths = [int(term_width * 0.48), int(term_width * 0.25), int(term_width * 0.25)]
    
    msg = f'{format_column(msg[0], widths[0])} {format_column(msg[1], widths[1])} {format_column(msg[2], widths[2])}'
    print(msg)


def get_address(id):
    return hashlib.sha256(str(id).encode()).hexdigest()


def get_raw_address(id):
    return get_address(id)[:33]


def get_raw_address_from_string(s):
    return s[:33]


def print_red(*args):
    print("\033[91m", end="")
    print(*args)
    print("\033[0m", end="")
