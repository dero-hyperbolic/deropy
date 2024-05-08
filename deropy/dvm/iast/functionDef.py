import json, ast, inspect

import deropy.dvm.iast as iast
import deropy.dvm.iast.iast_converter as iast_converter
from deropy.dvm.utils import type_python_to_intermediate, filter_args_out

code = 'store("owner", "signer")'
python_ast = ast.parse(code)

class FunctionDef(iast.IastNode):
    def __init__(self, name, args, body, returns):
        self.name = name
        self.args = args
        self.body = body
        self.returns = returns

    @classmethod
    def from_python_ast(cls, node, body: list):
        returns = node.returns.id if node.returns is not None else None
        iast_body = []
        for b in body:
            if isinstance(b, list):
                for l in b:
                    iast_body.append(l)
                continue
            iast_body.append(b)

        return cls(
            node.name,
            [iast_converter.to_iast(arg) for arg in node.args.args if filter_args_out(arg)],
            iast_body,
            returns
        )
    
    def add_to_body(self, node: iast.IastNode):
        self.body.append(node)

    def to_json(self):
        return json.dumps(
            {
                "type": "FunctionDef",
                "function": {
                    "name": self.name,
                    "args": [json.loads(arg.to_json()) for arg in self.args],
                    "body": [json.loads(n.to_json()) for n in self.body],
                    "returns": type_python_to_intermediate(self.returns)
                }
            }
        )

    def __repr__(self):
        return f"Function {self.name}({', '.join([str(arg) for arg in self.args])}) -> {self.returns}"
    