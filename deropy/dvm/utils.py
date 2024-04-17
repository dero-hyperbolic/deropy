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