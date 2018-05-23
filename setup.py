"""Setup flask-eztest."""

from setuptools import setup

requirements = [
    'Flask',
    'selenium',
    'Flask-SQLAlchemy'
]

description = "Flask test generation based on db models."

long_description = open('README.md').read()

setup(
    name='flaskeztest',
    version='0.1.0',
    author='Stanley Rokita',
    author_email='srok35@gmail.com',
    description=description,
    long_description=long_description,
    install_requires=requirements,
    packages=['flaskeztest'],
    entry_points={
        'console_scripts': [
            'eztest = flaskeztest.__main__:flaskeztest_main'
        ]
    }
)
