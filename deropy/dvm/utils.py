import hashlib
import functools

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

def flatten_list(l):
    output = []
    for i in l:
        if isinstance(i, list):
            output.extend(flatten_list(i))
        else:
            output.append(i)

    return output

def print_interpreter(msg: list):
    def format_column(content, width):
        if len(content) > width:
            content = content[:width-3] + "..."
        else:
            content = content + " " * (width - len(content))
        return content
    
    msg = f'{format_column(msg[0], 80)} {format_column(msg[1], 20)} {format_column(msg[2], 20)}'
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
    