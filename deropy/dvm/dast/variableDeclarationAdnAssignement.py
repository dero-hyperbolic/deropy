import json

from deropy.dvm.utils import type_python_to_intermediate


class VariableDeclarationAndAssignment():
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    @classmethod
    def from_intermediate_ast(cls, json_obj):
        return cls(json_obj["declaration"]["variable"]["name"], json_obj["declaration"]["variable"]["type"], json_obj["assignment"]["value"])
    
    def to_json(self):
        declaration = json.dumps(
             {
                "type": "VariableDeclaration",
                "variable": {
                    "name": self.name,
                    "type": type_python_to_intermediate(self.type),
                }
            }
        )
        assignment = json.dumps(
            {
                "type": "Assignment",
                "variable": self.name,
                "value": self.value
            }
        )
        
        return json.dumps(
            {
                "type": "VariableDeclarationAndAssignment",
                "declaration": json.loads(declaration),
                "assignment": json.loads(assignment)
            }
        )
    
    
    def __repr__(self):
        return f""