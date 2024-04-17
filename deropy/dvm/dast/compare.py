import json, ast, inspect

import deropy.dvm.iast as dast
import deropy.dvm.dast.dast_converter as dast_converter


class Compare():
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    @classmethod
    def from_intermediate_ast(cls, json_iast):
        left = dast_converter.to_dast(json_iast["left"])
        op = dast_converter.to_dast(json_iast["op"])
        right = dast_converter.to_dast(json_iast["right"])
        return cls(left, op, right)
    
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