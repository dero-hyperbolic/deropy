import os
from setuptools import setup, find_packages

setup(
    name='deropy',
    version=os.getenv('DEROPY_VERSION') or '0.2.0',
    url='https://github.com/dero-hyperbolic/deropy.git',
    author_email='leocances@gmail.com',
    description='A set of tool to help of DERO smart contract development',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'click==8.0.4',
        'requests==2.31.0',
        'coloredlogs==15.0.1',
        'pyperclip==1.8.2',
        'python-dotenv==0.20.0',
        'InquirerPy==0.3.4',
        'pycryptodome==3.20.0',
    ],
    include_package_data=True,
    package_data={},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'deropy=deropy.main:deropy'
        ]
    }
)
