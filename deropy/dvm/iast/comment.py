import json


import deropy.dvm.iast as iast


class Comment(iast.IastNode):
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_python_ast(cls, node):
        import ast
        print(ast.dump(node))
        return cls(node.value.value)

    def to_json(self):
        return json.dumps(
            {
                "type": "Comment",
                "value": self.value
            }
        )

    def __repr__(self):
        return f"{self.value}"