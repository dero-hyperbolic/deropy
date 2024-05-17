# {{project_name}}

This is a quick start guide that should provide you with the minimum to test and deploy your smart-contract

# Development

A smart-contract developed with `deropy` is a python class that inherits from `SmartContract`. The must **not** have a construction (`__init__`) method. A SC public function start with a Capital letter. A private function (not accessible through the API) starts with a lower case lette

- You can use `if`, `if else` condition, `while` loops and return statement.

- Each function parameter **must** be annotated, the function **must** have its return type annotated.

- Each variable you declare **must** be annotated

> The only annotation supported are either `int` (Uint64) or `str` (String)

here is an example of a simple smart-contract with a variable declaration

```python
class {{smartcontract_class}}(SmartContract):
    def Initialize(self) -> str:
        owner: str = signer()
        if check_owner(owner) == 1:
            # Do something
            return 0
        else:
            # Do something else
            return 0  # or 1 if error

    def check_owner(self, raw_addr: str) -> int:
        if raw_addr == signer():
            return 1
        return 0
```

# Tests

Your tests must be written using `pytest` (should possible to use other library, but it is up to you to discover how to).

Each function written in your deropy smart-contract are fully executable, hence the tests can simply be running using the following command

```bash
pytest tests/test_{{project_name}}.py -vx
```

# Transpile

The interesting part of `deropy` is that you can transpile your python smart-contract into a `dero` smart-contract. To do so, you need to run the following command

```bash
deropy transpile src/{{project_name}}.py
```

you will find the transpile `.bas` file into the `dist` folder


# Deploy

To deploy your transpiled smart-contract, you need to run the following command

```bash
deropy deploy dist/{{project_name}}.bas
```


# API Generate

To generate the API for your smart-contract, you need to run the following command

```bash
deropy generate dist/{{project_name}}.bas
```

You can also using the `deploy` command with the `--generate` flag to automatically generate the API after deploying the smart-contract. That way the file will be populated with the SC SCID

```bash
deropy deploy -g dist/{{project_name}}.bas
```


# Simulate

To deploy your smart-contract against the derohe simulator, you need to run the following command.

```bash
deropy simulate path/to/derohe_simulator src/{{project_name}}.py tests/test_{{project_name}}.py
```

It will automatically start the derohe simulator, transpile your python smart-contract, deploy it to the simulator, generate the API and then run the tests against the DEROHE simulator