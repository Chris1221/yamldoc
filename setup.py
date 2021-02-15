from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
   name='yamldoc',
   version='0.1.4',
   description='Documentation engine for YAML.',
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Chris Cole',
   author_email='ccole@well.ox.ac.uk',
   packages=['yamldoc'],  #same as name
   entry_points={
        'console_scripts': [
            'yamldoc = yamldoc:cli',
        ],
    }
)
