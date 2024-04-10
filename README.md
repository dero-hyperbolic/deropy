# DEROPY

Deropy is a toolbox for creating, managing and testing DERO smart contracts.

## Installation

```bash
pip install deropy
```

## Quick Start

**If the simulator is running** the followin
the following command will:
- Deploy your smart contract to the simulator
- Create a new SC.py file in the current directory with the correct SCID.
- A new tests/test_sc.py file in the current directory.

**If the simulator is not running** the Smart Contract will not be deployed

SC.py will contain a class that allow you to call every function implemented in your smart contract
test_sc.py will contain a test class that provide you with a basic test skeleton for every function implemented in your smart contract

```bash
deropy deploy -g path/to/sc.bas
```

## Commands

| Command | Description |
| --- | --- |
| `deropy init` | Initialize a new DERO project |
| `deropy deploy` | Compile a DERO smart contract |
| `deropy generate` | Test a DERO smart contract |


