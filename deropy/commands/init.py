import requests
import os, shutil
import click
import InquirerPy

from deropy.commands.generate import _generate_class, _generate_tests

@click.command('init')
def init():
    # ask for the smart contract name
    questions = {"type": "input", "name": "sc_name", "message": "Enter the smart contract name:"}
    answers = InquirerPy.prompt(questions)
    sc_name = answers['sc_name']

    # What template to use
    template_list = os.listdir('deropy/templates')
    questions = {"type": "list", "name": "template", "message": "Select the template to use:", "choices": template_list}
    answers = InquirerPy.prompt(questions)
    template = answers['template']

    # Create the smart contract folder
    os.makedirs(sc_name, exist_ok=True)
    
    # Copy the template to the smart contract folder
    shutil.copytree(f'deropy/templates/{template}', f'{sc_name}/{template}')
    
if __name__ == '__main__':
    init()