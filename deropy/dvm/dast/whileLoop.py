import json, ast, inspect

import deropy.dvm.dast as dast
import deropy.dvm.dast.dast_converter as dast_converter


class WhileLoop():
    def __init__(self, compare, body):
        self.compare = compare
        self.body = body

    @classmethod
    def from_intermediate_ast(cls, json_iast):
        return cls(
            dast_converter.to_dast(json_iast["compare"]),
            [dast_converter.to_dast(n) for n in json_iast["body"][0]],  # for some reason the body of a While is [[]]
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
        return ""