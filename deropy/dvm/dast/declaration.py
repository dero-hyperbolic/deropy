import json

import deropy.dvm.dast.dast_converter as dast_converter
from deropy.dvm.utils import type_intermediate_to_dvm


class VariableDeclaration():
    def __init__(self, name, type):
        self.name = name
        self.type = type

    @classmethod
    def from_intermediate_ast(cls, json):
        return cls(
            dast_converter.to_dast(json["variable"]["name"]),
            dast_converter.to_dast(json["variable"]["type"])
        )

    def to_json(self):
        return json.dumps(
            {
                "type": "VariableDeclaration",
                "variable": {
                    "name": self.name,
                    "type": self.type
                }
            }
        )
    
    def __repr__(self):
        return f"DIM {self.name} AS {type_intermediate_to_dvm(str(self.type))}"
