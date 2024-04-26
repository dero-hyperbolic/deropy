import json, ast, inspect


class Goto():
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_intermediate_ast(cls, json_obj):
        return cls(json_obj["value"])

    def to_json(self):
        return json.dumps(
            {
                "type": "Goto",
                "value": self.value
            }
        )

    def __repr__(self):
        return f"GOTO {self.value}"