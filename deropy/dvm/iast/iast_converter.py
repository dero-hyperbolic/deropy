import ast

import deropy.dvm.iast as iast


def to_iast(node):
    if isinstance(node, list):
        return [to_iast(n) for n in node]

    if isinstance(node, ast.ClassDef):
        pass

    if isinstance(node, ast.If):
        return iast.IfTest.from_python_ast("if", node)

    if isinstance(node, ast.While):
        return iast.WhileLoop.from_python_ast(node)

    if isinstance(node, ast.Compare):
        return iast.Compare.from_python_ast(node)

    if isinstance(node, ast.BinOp):
        return iast.BinaryOperator.from_python_ast(node)

    if isinstance(node, ast.arg):
        return iast.Argument.from_python_ast(node)

    if isinstance(node, ast.Assign):
        return iast.Assignment.from_python_ast(node)

    if isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            return iast.VariableDeclarationAndAssignment.from_python_ast(node)

    if isinstance(node, ast.Call):
        return iast.FunctionCall.from_python_ast(node)

    if isinstance(node, ast.Expr):
        if isinstance(node.value, ast.Call):
            return iast.FunctionCall.from_python_ast(node.value)

    if isinstance(node, ast.FunctionDef):
        body = []
        for b in node.body:
            p = to_iast(b)
            if p is not None:
                body.append(p)

        return iast.FunctionDef.from_python_ast(node, body)

    if isinstance(node, ast.Return):
        return iast.Return.from_python_ast(node)

    # LEAF
    if isinstance(node, ast.Constant):
        return iast.Constant.from_python_ast(node)

    if isinstance(node, ast.Name):
        return iast.Name.from_python_ast(node)

    # OPERATORS
    if isinstance(node, ast.Eq):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.NotEq):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.Lt):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.LtE):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.Gt):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.GtE):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.Is):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.IsNot):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.Add):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.Sub):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.Mult):
        return iast.Operator.from_python_ast(node)
    if isinstance(node, ast.Div):
        return iast.Operator.from_python_ast(node)

    raise Exception(f'Unknown node type: {type(node)}')