import requests
import click
import py

from commands.generate import _generate_class, _generate_tests

@click.command('init')
@click.argument('file', type=click.Path())
@click.option('-g', '--generate', is_flag=True, help='Generate the SC file')
def init(file, generate):
    sc_txid = _deploy(file)
    click.echo(f'Transaction ID: {sc_txid}')

    if generate:
        _generate_class(file, sc_txid)
        _generate_tests(file)
