import requests
import click

from deropy.commands.generate import _generate_class, _generate_tests


@click.command('deploy')
@click.argument('file', type=click.Path())
@click.option('-g', '--generate', is_flag=True, help='Generate the SC file')
def deploy(file, generate):
    sc_txid = _deploy(file)
    click.echo(f'Transaction ID: {sc_txid}')

    if generate:
        _generate_class(file, sc_txid)
        _generate_tests(file)


def _deploy(file: str):
    with open(file, 'r') as f:
        data = f.read()

    url = 'http://127.0.0.1:30000/install_sc'
    response = requests.post(url, data.encode())

    data = response.json()
    return data['txid']
