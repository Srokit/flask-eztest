"""Setup flask-eztest."""

from setuptools import setup, find_packages

requirements = [
    'Flask',
    'selenium'
]

description = "Flask test generation based on db models."

long_description = open('README.md').read()

classifiers = [
        'Development Status :: 1 - Development',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
]

setup(
    name='flaskeztest',
    version='0.1.0',
    author='Stanley Rokita',
    author_email='srok35@gmail.com',
    description=description,
    long_description=long_description,
    install_requires=requirements,
    packages=find_packages(exclude=['test']),
    classifiers=classifiers
)
