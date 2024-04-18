import inspect, json, ast, sys

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

def parse(path):
    parsed = file_to_iast(path)
    
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

            # If the block is an IfTest
            # 1. Pop and append the if block to the end of the function
            # 2. Replace the if body with a Goto to the end of the function
            # 3. increment the function body size
            # 4. Repeat 1, 2 and 3 with the else block
            if b["type"] == "IfTest" and b["mode"] == "if":
                if_body = flatten_list(b["if_body"])
                else_body = flatten_list(b["else_body"])
                before_if = flatten_func_body[:i+1]
                after_if = flatten_func_body[i+1:]
            
                b["if_body"] = [json.loads(dast.Name(len(before_if) + 1).to_json())]
                before_if.extend(if_body)
                before_if.extend([json.loads(dast.Goto(len(before_if) + len(else_body)).to_json())])

                if len(else_body) > 0:
                    b["else_body"] = [json.loads(dast.Name(len(before_if) + 1).to_json())]
                    before_if.extend(else_body)

                
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
        print(f'End Function\n')