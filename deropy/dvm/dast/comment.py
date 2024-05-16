import json, ast, inspect


class Comment():
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_intermediate_ast(cls, json_obj):
        return cls(json_obj["value"])

    def to_json(self):
        return json.dumps(
            {
                "type": "Comment",
                "value": self.value
            }
        )

    def __repr__(self):
        if '\n' in self.value:
            lines = self.value.split('\n')
            return '\n'.join(['// ' + line for line in lines])

        return f"// {self.value}"