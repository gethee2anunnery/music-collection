try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Playlist Manager',
    'author': 'Sara Perry',
    'url': '',
    'author_email': 'paraserry@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['playlist'],
    'scripts': [],
    'name': 'Playlist Manager'
}

setup(**config)
