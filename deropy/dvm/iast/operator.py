import json, ast, inspect

import deropy.dvm.iast as iast
import deropy.dvm.iast.iast_converter as iast_converter


class Operator(iast.IastNode):
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_python_ast(cls, node):
        if isinstance(node, ast.Eq):
            return cls("==")._invert()
        if isinstance(node, ast.NotEq):
            return cls("!=")._invert()
        if isinstance(node, ast.Lt):
            return cls("<")._invert()
        if isinstance(node, ast.LtE):
            return cls("<=")._invert()
        if isinstance(node, ast.Gt):
            return cls(">")._invert()
        if isinstance(node, ast.GtE):
            return cls(">=")._invert()
        if isinstance(node, ast.Is):
            return cls("is")._invert()
        if isinstance(node, ast.IsNot):
            return cls("is not")._invert()
        if isinstance(node, ast.Add):
            return cls("+")._invert()
        if isinstance(node, ast.Sub):
            return cls("-")._invert()
        if isinstance(node, ast.Mult):
            return cls("*")._invert()
        if isinstance(node, ast.Div):
            return cls("/")._invert()
        else:
            raise ValueError(f"Unknown operator: {node}")
        
    def _invert(self):
        if self.value == "==":
            self.value = "!="
        elif self.value == "!=":
            self.value = "=="
        elif self.value == "<":
            self.value = ">="
        elif self.value == "<=":
            self.value = ">"
        elif self.value == ">":
            self.value = "<="
        elif self.value == ">=":
            self.value = "<"
        elif self.value == "is":
            self.value = "is not"
        elif self.value == "is not":
            self.value = "is"
        return self

    def to_json(self):
        return json.dumps(
            {
                "type": "Operator",
                "value": self.value
            }
        )

    def __repr__(self):
        return f"{self.value}"