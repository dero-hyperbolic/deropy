import click
from InquirerPy import prompt
import shutil
import os
import inspect


@click.command('create')
def create():
    questions = [
        {
            "type": "input",
            "message": "What is your project named?",
            "name": "project_name",
            "default": "my_sc"
        },
        {
            "type": "confirm",
            "message": "Would you like to start with minimal smart contract?",
            "name": "minimal",
            "default": True,
        },
        {
            "type": "confirm",
            "message": "Would you like to setup basic tests?",
            "name": "tests",
            "default": True,
        }
    ]

    results = prompt(questions)
    return _create(**results)


def _create(project_name: str, minimal: bool, tests: bool):
    np = lambda *args : os.path.join(os.path.dirname(os.path.dirname(__file__)), *args)
    nd = lambda *args : os.makedirs(np(*args))

    if os.path.exists(project_name):
        click.echo(f"Project {project_name} already exists")
        return

    shutil.copytree(np('data', 'new_project_template'), project_name)

    if not minimal:
        os.remove(os.path.join(project_name, 'src', 'project_name.py'))

    if not tests:
        os.remove(os.path.join(project_name, 'tests', 'test_project_name.py'))
        
    # replace all occurences of project_name in the project with the project name
    for root, dirs, files in os.walk(project_name):
        for f in files:
            if f.endswith('.py') or f.endswith('.md'):
                with open(os.path.join(root, f), 'r') as _f:
                    content = _f.read()

                new_file_name = f
                if "project_name" in f:
                    new_file_name = f.replace("project_name", project_name)

                smartcontract_class = project_name.capitalize()
                smartcontract_class = smartcontract_class.replace("_", "")

                with open(os.path.join(root, new_file_name), 'w') as _f:
                    n_content = content.replace('{{project_name}}', project_name)
                    n_content = n_content.replace('{{smartcontract_class}}', smartcontract_class)
                    _f.write(n_content)

                if "readme" not in f:
                    os.remove(os.path.join(root, f))

    click.echo(f"Project {project_name} created")
