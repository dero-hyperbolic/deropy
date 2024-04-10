import os
from setuptools import setup, find_packages

setup(
    name='solwr',
    version=os.getenv('SOLWR_VERSION') or '1.0.0',
    url='https://gitlab.driw.no/platform/solwr-helper',
    author_email='leo.cances@solwr.com',
    description='A set of tool that suppose to help with SOLWR projects',
    packages=find_packages(),
    install_requires=[
        'click==8.0.4',
        'xmltodict==0.13.0',
        'requests==2.27.1',
        'coloredlogs==15.0.1',
        'pyperclip==1.8.2',
        'python-dotenv==0.20.0',
        'InquirerPy==0.3.4',
    ],
    include_package_data=True,
    package_data={
        'solwr': [
            'bash_scripts/*',
            'bash_scripts/**/*',
            'bash_scripts/.env.template',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'solwr=solwr.main:solwr'
        ]
    }
)
