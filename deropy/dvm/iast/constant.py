import json, ast, inspect

import deropy.dvm.iast as iast
import deropy.dvm.iast.iast_converter as iast_converter


class Constant(iast.IastNode):
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_python_ast(cls, node):
        return cls(node.value)

    def to_json(self):
        return json.dumps(
            {
                "type": "Constant",
                "value": self.value
            }
        )

    def __repr__(self):
        return f"{self.value}"