import json

from deropy.dvm.utils import type_python_to_intermediate
import deropy.dvm.iast as iast
import deropy.dvm.iast.iast_converter as iast_converter


class VariableDeclarationAndAssignment():
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    @classmethod
    def from_python_ast(cls, node):
        return cls(
            iast_converter.to_iast(node.target),
            iast_converter.to_iast(node.annotation),
            iast_converter.to_iast(node.value)
        )
    
    def to_json(self):
        return json.dumps([
             {
                "type": "VariableDeclaration",
                "variable": {
                    "name": json.loads(self.name.to_json()),
                    "type": json.loads(self.type.to_json()),
                }
            },
            {
                "type": "Assignment",
                "name": json.loads(self.name.to_json()),
                "value": json.loads(self.value.to_json())
            }
        ])
    
    def __repr__(self):
        return f"{self.name}: {self.type} = {self.value}"