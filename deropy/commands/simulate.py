import click
import subprocess
import logging


from deropy.commands.deploy import _deploy
from deropy.commands.generate import _generate


@click.command('simulate')
@click.argument('simulator', type=click.Path())
@click.argument('sc_file', type=click.Path())
@click.argument('tests_file', type=click.Path())
def simulate(simulator, sc_file, tests_file):
    _simulate(simulator, sc_file, tests_file)


def check(simulator: str, sc_file: str, tests_file: str):
    if not sc_file.endswith('.py'):
        logging.error('The smart contract file must be a python file')
        return False

    if not tests_file.endswith('.py'):
        logging.error('The tests file must be a python file')
        return False

    return True


def _simulate(simulator, sc_file, tests_file):
    if not check(simulator, sc_file, tests_file):
        return

    # execute the simulator in a subprocess
    subprocess.run([simulator])

    # use deropy to transpile the python smart-contract into a DVM-BASIC smart contract
    _generate(sc_file)

    # use deropy to deploy the smart contract
    _deploy(sc_file)

    # execute the tests file