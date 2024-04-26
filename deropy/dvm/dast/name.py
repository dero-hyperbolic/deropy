import json, ast, inspect


class Name():
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_intermediate_ast(cls, json_obj):
        return cls(json_obj["value"])

    def to_json(self):
        return json.dumps(
            {
                "type": "Constant",
                "value": self.value
            }
        )

    def __repr__(self):
        return f"{self.value}"