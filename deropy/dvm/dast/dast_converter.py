import deropy.dvm.dast as dast

def to_dast(json_object: dict):
    if isinstance(json_object, (str, int)):
        return json_object
    
    type_mapping = {
        "FunctionDef": dast.FunctionDef.from_intermediate_ast,
        "FunctionCall": dast.FunctionCall.from_intermediate_ast,
        "Constant": dast.Constant.from_intermediate_ast,
        "Name": dast.Name.from_intermediate_ast,
        "Return": dast.Return.from_intermediate_ast,
        "Compare": dast.Compare.from_intermediate_ast,
        "IfTest": dast.IfTest.from_intermediate_ast,
        "Operator": dast.Operator.from_intermediate_ast,
        "Argument": dast.Argument.from_intermediate_ast,
        "BinaryOperator": dast.BinaryOperator.from_intermediate_ast,
        "Assignment": dast.Assignment.from_intermediate_ast,
        "Goto": dast.Goto.from_intermediate_ast,
        "WhileLoop": dast.WhileLoop.from_intermediate_ast,
    }
    json_type = json_object["type"]
    if json_type in type_mapping:
        return type_mapping[json_type](json_object)
    else:
        raise Exception(f"Unknown type: {json_type}")
