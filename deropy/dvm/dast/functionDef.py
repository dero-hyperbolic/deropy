import json, ast, inspect

import deropy.dvm.dast as dast
import deropy.dvm.dast.dast_converter as dast_converter
from deropy.dvm.utils import type_intermediate_to_dvm


class FunctionDef():
    def __init__(self, name, args, body, returns):
        self.name = name
        self.args = args
        self.body = body
        self.returns = returns

    @classmethod
    def from_intermediate_ast(cls, json):
        return cls(
            json["function"]["name"],
            [dast_converter.to_dast(arg) for arg in json["function"]["args"]],
            json["function"]["body"],
            json["function"]["returns"]
        )
    
    def to_json(self):
        return json.dumps(
            {
                "type": "FunctionDef",
                "function": {
                    "name": self.name,
                    "args": [arg for arg in self.args],
                    "body": self.body,
                    "returns": self.returns
                }
            }
        )
    
    def __repr__(self):
        return f"Function {self.name}({', '.join([str(arg) for arg in self.args])}) {type_intermediate_to_dvm(self.returns)}"
    