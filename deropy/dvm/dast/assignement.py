import json

import deropy.dvm.dast.dast_converter as dast_converter


class Assignment():
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    @classmethod
    def from_intermediate_ast(cls, json):
        return cls(
            dast_converter.to_dast(json["name"]),
            dast_converter.to_dast(json["value"])
        )

    def to_json(self):
        return json.dumps(
            {
                "type": "Assignment",
                "name": self.variable,
                "value": self.value
            }
        )

    def __repr__(self):
        return f"LET {self.variable} = {str(self.value)}"