import json, ast, inspect

import deropy.dvm.iast as iast
import deropy.dvm.iast.iast_converter as iast_converter


class FunctionCall(iast.IastNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    @classmethod
    def from_python_ast(cls, node):
        return cls(node.func.id, [iast_converter.to_iast(arg) for arg in node.args])

    def to_json(self):
        json_args = []
        for a in self.args:
            json_args.append(json.loads(a.to_json()))

        return json.dumps(
            {
                "type": "FunctionCall",
                "function": {
                    "name": self.name,
                    "args": json_args
                }
            }
        )

    def __repr__(self):
        return f"{self.name}({', '.join([str(arg) for arg in self.args])})"
    