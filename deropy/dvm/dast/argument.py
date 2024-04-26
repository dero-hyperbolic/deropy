import json, ast, inspect

import deropy.dvm.iast as dast
import deropy.dvm.dast.dast_converter as dast_converter
from deropy.dvm.utils import type_intermediate_to_dvm


class Argument():
    def __init__(self, name, type):
        self.name = name
        self.type = type

    @classmethod
    def from_intermediate_ast(cls, json_obj):
        return cls(json_obj["name"], dast_converter.to_dast(json_obj["ntype"]))

    def to_json(self):
        return json.dumps(
            {
                "type": "Argument",
                "name": self.name,
                "type": json.loads(self.type.to_json())
            }
        )
    
    def __repr__(self):
        return f"{self.name} {type_intermediate_to_dvm(str(self.type))}"