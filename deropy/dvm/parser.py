import inspect
import json
import ast
import sys

import deropy.dvm.iast.iast_converter as iast_converter
import deropy.dvm.dast as dast
from deropy.dvm.dast import *
from deropy.dvm.utils import flatten_list


def load_dast(str_func_name, obj):
    return globals()[str_func_name].from_intermediate_ast(obj)


def file_to_iast(path):
    with open(path, "r") as f:
        code = f.readlines()

    # remove all lines that are comments, or imports
    code = [line for line in code if not line.startswith("#") and not line.startswith("import") and not line.startswith("from")]
    code = [line for line in code if line.strip() != ""]

    # remove all str( ... ) call but keep what's inside the parenthesis
    i = 0
    while i < len(code):
        line = code[i]
        if 'str(' in line:
            start = line.index('str(')
            end = line.index(')', start)
            inside = line[start+4:end]
            code[i] = line[:start] + inside + line[end+1:]
        i += 1

    code = "".join(code)
    tree = ast.parse(code)

    return tree_to_iast(tree)


def code_to_iast(code):
    tree = ast.parse(code)
    return tree_to_iast(tree)


def tree_to_iast(tree):
    parsed = []
    for i, node in enumerate(tree.body[0].body):
        p = iast_converter.to_iast(node)
        if p is not None:
            parsed.append(p)

    return parsed


def parse(path, output_path=None):
    parsed = file_to_iast(path)

    # if output_path exists, overwrite it
    if output_path is not None:
        with open(output_path, 'w') as f:
            f.write('')

    for f in parsed:
        func_dvm = []

        json_function = json.loads(f.to_json())

        func = load_dast(json_function["type"], json_function)
        flatten_func_body = []
        for b in func.body:
            if isinstance(b, list):
                for l in b:
                    flatten_func_body.append(l)
                continue
            flatten_func_body.append(b)

        i = 0
        while i < len(flatten_func_body):
            b = flatten_func_body[i]

            # If the block is an IfTest, we need to do some special handling
            if b["type"] == "IfTest" and b["mode"] == "if":
                if_body = flatten_list(b["if_body"])
                else_body = flatten_list(b["else_body"])
                before_if = flatten_func_body[:i+1]
                after_if = flatten_func_body[i+1:]

                # Compute the if and else block
                if_body_position = len(before_if) + 1
                else_body_position = if_body_position + len(if_body)

                # replace the if and else body with Goto position
                b["if_body"] = [json.loads(dast.Name(if_body_position).to_json())]
                b["else_body"] = [json.loads(dast.Name(else_body_position).to_json())]

                # Append the if and else body right after the if block
                before_if.extend(if_body)
                before_if.extend(else_body)

                # finish the if block
                before_if.extend(after_if)
                flatten_func_body = before_if

            # If the block is a WhileLoop
            # 1. Pop and append the while block right after the while block
            # 2. Replace the while block with a IfTest that use the compare of the while block and goto after the while block
            if b["type"] == "WhileLoop":
                original_position = i
                if_json_iast = {
                    "type": "IfTest",
                    "mode": "while",
                    "condition": b["compare"],
                    "if_body": [json.loads(dast.Name(original_position + 1).to_json())],
                    "else_body": []
                }

                before_while = flatten_func_body[:i]
                after_while = flatten_func_body[i+1:]
                before_while.extend(flatten_list(b["body"]))
                before_while.append(if_json_iast)
                before_while.extend(after_while)
                flatten_func_body = before_while

            i += 1

        # print the DVM-BASIC code
        print(func)
        for i, b in enumerate(flatten_func_body):
            print(f'{i+1} {load_dast(b["type"], b)}')
        print('End Function\n')

        # Write the DVM-BASIC code to a file
        if output_path is None:
            output_path = path.split('.')[0] + '.bas'

        with open(output_path, 'a') as f:
            f.write(f'{func}\n')
            for i, b in enumerate(flatten_func_body):
                f.write(f'{i+1} {load_dast(b["type"], b)}\n')
            f.write('End Function\n\n')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser.py <path_to_file>")
        sys.exit(1)

    print('\n')
    print('-'*50)
    print('\n')
    parse(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
    print('-'*50)
    print('\n')
