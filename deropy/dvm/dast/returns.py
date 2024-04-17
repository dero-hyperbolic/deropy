import json, ast, inspect

import deropy.dvm.dast.dast_converter as dast_converter


class Return():
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_intermediate_ast(cls, json_obj):
        return cls(dast_converter.to_dast(json_obj["value"]))

    def to_json(self):
        return json.dumps(
            {
                "type": "Return",
                "value": json.loads(self.value.to_json())
            }
        )

    def __repr__(self):
        return f"RETURN {self.value}"