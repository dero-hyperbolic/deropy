import json, ast, inspect

import deropy.dvm.iast as dast
import deropy.dvm.dast.dast_converter as dast_converter


class Operator():
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_intermediate_ast(cls, json_iast):
        return cls(json_iast["value"])

    def to_json(self):
        return json.dumps(
            {
                "type": "Operator",
                "value": self.value
            }
        )

    def __repr__(self):
        return f"{self.value}"