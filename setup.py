try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Lil Python project',
    'author': 'Sara Perry',
    'url': '',
    'author_email': 'paraserry@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['collection'],
    'scripts': [],
    'name': 'Music Collection Manager'
}

setup(**config)
