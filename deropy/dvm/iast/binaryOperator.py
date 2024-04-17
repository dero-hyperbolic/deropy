import json, ast, inspect

import deropy.dvm.iast as iast
import deropy.dvm.iast.iast_converter as iast_converter


class BinaryOperator(iast.IastNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    @classmethod
    def from_python_ast(cls, node):
        return cls(
            iast_converter.to_iast(node.left),
            iast_converter.to_iast(node.op),
            iast_converter.to_iast(node.right)
        )

    def to_json(self):
        return json.dumps(
            {
                "type": "Compare",
                "left": json.loads(self.left.to_json()),
                "op": json.loads(self.op.to_json()),
                "right": json.loads(self.right.to_json())
            }
        )

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"