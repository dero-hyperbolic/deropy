import json, ast, inspect

import deropy.dvm.iast as iast
import deropy.dvm.iast.iast_converter as iast_converter


class WhileLoop(iast.IastNode):
    def __init__(self, compare, body):
        self.compare = compare
        self.body = body

    @classmethod
    def from_python_ast(cls, node):
        return cls(
            iast_converter.to_iast(node.test),
            [iast_converter.to_iast(n) for n in node.body], # for some reason the body of a While is [[]]
        )

    def to_json(self):
        return json.dumps(
            {
                "type": "WhileLoop",
                "compare": json.loads(self.compare.to_json()),
                "body": [json.loads(n.to_json()) for n in self.body],
            }
        )

    def __repr__(self):
        return f"while {self.compare}:\n {self.body}"