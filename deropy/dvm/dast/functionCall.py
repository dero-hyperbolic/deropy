import json, ast, inspect

import deropy.dvm.dast.dast_converter as dast_converter


class FunctionCall():
    def __init__(self, name, args):
        self.name = name
        self.args = args

    @classmethod
    def from_intermediate_ast(cls, json_iast):
        args = []
        for a in json_iast["function"]["args"]:
            if isinstance(a, dict):
                args.append(dast_converter.to_dast(a))
                continue
            
            args.append(a)
        return cls(json_iast["function"]["name"], args)
    
    def to_json(self):
        json_args = []
        for a in self.args:
            if isinstance(a, FunctionCall):
                json_args.append(json.loads(a.to_json()))
                continue
            
            json_args.append(a)

        return json.dumps(
            {
                "type": "FunctionCall",
                "function": {
                    "name": self.name,
                    "args": json_args
                }
            }
        )
    
    def __str__(self):
        str_args = []
        for a in self.args:
            if isinstance(a, str):
                str_args.append(f'"{a}"')
                continue
        
            str_args.append(str(a))
        
        return f"{self.name.upper()}({', '.join([a for a in str_args])})"
    
    def __repr__(self):
        return str(self)
        
