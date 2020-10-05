from setuptools import setup

setup(
   name='yamldoc',
   version='0.1.1',
   description='Documentation engine for YAML.',
   author='Chris Cole',
   author_email='ccole@well.ox.ac.uk',
   packages=['yamldoc'],  #same as name
   entry_points={
        'console_scripts': [
            'yamldoc = yamldoc:cli',
        ],
    }
)
