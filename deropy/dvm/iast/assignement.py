import json

import deropy.dvm.iast.iast_converter as iast_converter


# python ast equivalent:
# Assign(targets=[Name(id='a', ctx=Store())], value=Constant(value=0))

class Assignment():
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @classmethod
    def from_python_ast(cls, node):
        return cls(node.targets[0].id, iast_converter.to_iast(node.value))

    def to_json(self):
        return json.dumps([
            {
                "type": "Assignment",
                "name": self.name,
                "value": json.loads(self.value.to_json())
            }
        ])
    
    def __repr__(self):
        return f"{self.name}: {self.type} = {self.value}"