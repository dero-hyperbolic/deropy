import click
import os


simulator_host = 'http://127.0.0.1:30000'


@click.command('generate')
@click.argument('file', type=click.Path())
@click.option('-s', '--scid', type=str, help='The SCID of the smart contract', default='')
@click.option('--network', type=click.Choice(['simulator', 'mainnet']), default='simulator')
@click.option('-o', '--output', type=click.Path(), help='The output file')
def generate(file, scid, network, output):
    _generate(file, scid, network, output)


def _generate(file, scid, network, output):
    host = simulator_host

    _generate_class(file, scid, output)
    # _generate_tests(file


def _generate_tests(file):
    file_content = _read_bas(file)
    functions = _parse_function(file_content)

    lines = ['from SC import SC']
    lines += ['import unittest']
    lines += ['', '']
    lines += ['class TestSC(unittest.TestCase):']
    lines += ['']
    lines += ['    def setUp(self):']
    lines += ['        self.SC = SC()']
    lines += ['']

    for f, p in functions.items():
        test_method = _generate_test_method(f, p)
        lines.extend(test_method)

    os.makedirs('tests', exist_ok=True)
    with open('tests/test_SC.py', 'w') as f:
        for line in lines:
            f.write(f'{line}\n')


def _generate_test_method(f_name, p):
    lines = [f'\n    def test_{f_name}(self):']

    # Create a parameter map
    if len(p) != 0:
        lines += ['        params = {']
        for k, v in p.items():
            lines += [f'            "{k}": {_SC_type_to_python_fake(v)},']
        lines += ['        }']
        lines += ['']

    # Create the tempalte for expected response
    lines += ['        # ---- Expected response or SC content']
    lines += ['        expected_response = {']
    lines += ['            "jsonrpc": "2.0",']
    lines += ['            "id": "1",']
    lines += ['        }']
    lines += ['']

    # Create the method call
    lines += ['        # ---- Invoke the SC function (use the commented line if you need to setup fee)']
    if len(p) > 0:
        lines += [f'        response_json = SC.{f_name}(**params)']
        lines += [f'        #response_json = SC.{f_name}_fee(1000, **params)']
    else:
        lines += [f'        response_json = SC.{f_name}()']
        lines += [f'        #response_json = SC.{f_name}_fee(1000)']

    lines += ['']

    # Read the smart contract (could be needed to check variables)
    lines += ['        # ---- Read the smart contract (could be needed to check variables)']
    lines += ['        sc_content = self.sc.read()']
    lines += ['']

    # Create the assertion
    lines += ['        # ---- Your test here']
    lines += ['        self.assertEqual(1, 1)']

    return lines


def _generate_class(file: str, scid: str, output: str = None):
    file_content = _read_bas(file)
    functions = _parse_function(file_content)

    output_path = output if output is not None else 'SC.py'

    class_name = os.path.basename(file)
    class_name = class_name.split('.')[0]
    class_name = class_name.capitalize()

    lines = ['import requests']
    lines += ['import json\n']
    lines += [f'class {class_name}:']
    lines += [f'    SCID="{scid}"']
    lines += ['    def __init__(self):']
    lines += [f"        self.url = '{simulator_host}/json_rpc'"]
    lines += ["        self.headers = {'content-type': 'application/json'}"]
    lines += ['']
    lines.extend(_generate_read_method(scid))
    for f, p in functions.items():
        scinvoce_method = _generate_method_scinvoce(f, p, class_name)
        # transfer2_method = _generate_method_transfer2(f, p)
        lines.extend(scinvoce_method)
        # lines.extend(transfer2_method)

    with open(output_path, 'w') as f:
        for line in lines:
            f.write(f'{line}\n')


def _read_bas(path: str) -> str:
    with open(path, 'r') as f:
        return f.readlines()


def _parse_function(lines: list) -> dict:
    def get_function_name(line: str) -> str:
        return line[9:].split('(')[0]

    def get_function_parameters(line: str) -> list:
        output = dict()
        parameters = line[9:].split('(')[1].split(')')[0].split(',')
        if len(parameters) == 1 and parameters[0] == '':
            return output

        for p in parameters:
            p = p.strip()
            output[p.split()[0]] = p.split()[1]

        return output

    functions = {}
    for line in lines:
        if "Function " in line and "End Function" not in line:
            function_name = get_function_name(line)

            if not function_name[0].isupper():
                continue

            parameters = get_function_parameters(line)
            functions[function_name] = parameters

    return functions


def _generate_read_method(scid):
    return [
        '    def read(self):',
        '        url = "http://127.0.0.1:20000/json_rpc"',
        '        payload = {',
        '            "jsonrpc": "2.0",',
        '            "id": "1",',
        '            "method": "DERO.GetSC",',
        '            "params": {',
        f'                "scid": "{scid}",',
        '                "code": True,',
        '                "variables": True',
        '            }',
        '        }',
        '        response = requests.post(url, data=json.dumps(payload), headers=self.headers)',
        '        # keep only the `stringkeys` and `variables`',
        '        data = response.json()',
        '        self.storage = data["result"]["stringkeys"]',
        '        return self.storage',
    ]


def _generate_method_scinvoce(f_name, p, class_name):
    # create the method definition
    method_parameters = ''
    for k, v in p.items():
        method_parameters += f'{k}: {_SC_type_to_python_type(v)}, '
    method_parameters = method_parameters[:-2]

    if len(method_parameters) == 0:
        lines = [f'\n    def {f_name}(self, dero_deposit: int = 0, asset_deposit: int = 0, host: str = None):']
    else:
        lines = [f'\n    def {f_name}(self, {method_parameters}, dero_deposit: int = 0, asset_deposit: int = 0, host: str = None):']

    scrpc = [
        '                    "sc_rpc": [',
        '                        {',
        '                            "name": "entrypoint",',
        '                            "datatype": "S",',
        f'                            "value": "{f_name}"',
        '                        },',
    ]

    for k, v in p.items():
        scrpc += [
            '                        {',
            f'                            "name": "{k}",',
            f'                            "datatype": "{_SC_type_to_jsonrpc(v)}",',
            f'                            "value": {k}',
            '                        },',
        ]

    payload = [
        '        payload = {',
        '                "jsonrpc": "2.0",',
        '                "id": "1",',
        '                "method": "scinvoke",',
        '                "params": {',
        f'                    "scid": {class_name}.SCID,',
        '                    "ringsize": 2,',
    ]
    if f_name != 'Initialize':
        payload += [
            '                    "sc_dero_deposit": dero_deposit,',
            '                    "sc_asset_deposit": asset_deposit,',
        ]
    payload += scrpc
    payload += [
        '                    ]',
        '                }',
        '            }',
    ]
    lines.extend(payload)
    lines += [
        '        import pprint',
        '        pprint.pprint(payload)',
        '        url = self.url if host is None else host',
        '        print(f"using url {url}")',
        '        response = requests.post(url, data=json.dumps(payload), headers=self.headers)',
        '        pprint.pprint(response.json())']
    return lines


def _generate_method_transfer2(f_name, p):
    # create the method definition
    method_parameters = ''
    for k, v in p.items():
        method_parameters += f'{k}:{_SC_type_to_python_type(v)}, '
    method_parameters = method_parameters[:-2]

    if len(method_parameters) == 0:
        lines = [f'\n    def {f_name}_fee(self, fee: int):']
    else:
        lines = [f'\n    def {f_name}_fee(self, fee: int, {method_parameters}):']

    scrpc = [
        '                    "sc_rpc": [',
        '                        {',
        '                            "name": "entrypoint",',
        '                            "datatype": "S",',
        f'                            "value": "{f_name}"',
        '                        },',
    ]

    for k, v in p.items():
        scrpc += [
            '                        {',
            f'                            "name": "{k}",',
            f'                            "datatype": "{_SC_type_to_jsonrpc(v)}",',
            f'                            "value": {k}',
            '                        },',
        ]

    payload = [
        '        payload = {',
        '                "jsonrpc": "2.0",',
        '                "id": "1",',
        '                "method": "transfer",',
        '                "params": {',
        '                    "scid": SC.SCID,',
        '                    "ringsize": 2,',
        '                    "fees": fee,',
    ]
    payload += scrpc
    payload += [
        '                    ]',
        '                }',
        '            }',
    ]
    lines.extend(payload)
    lines += ['        response = requests.post(self.url, data=json.dumps(payload), headers=self.headers)']
    lines += ['        print(response.json())']
    return lines


def _SC_type_to_python_type(t: str):
    if t == 'String':
        return 'str'

    if t == 'Uint64':
        return 'int'
    raise RuntimeError(f'type [{t}] do not exist in DERO')


def _SC_type_to_python_fake(t: str):
    if t == 'String':
        return '"string"'

    if t == 'Uint64':
        return '1'
    raise RuntimeError(f'type [{t}] do not exist in DERO')


def _SC_type_to_jsonrpc(t: str):
    if t == "String":
        return "S"
    if t == "Uint64":
        return "U"
    raise RuntimeError(f'type {t} do not exist in DERO')

