import os
from distutils.core import setup

VERSION = '0.1'

classifiers = [
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Environment :: Web Environment",
]

setup(
    name='pycloudapp',
    version=VERSION,
    url='https://github.com/originell/pycloudapp',
    author='Luis Nell',
    packages=['cloudapp'],
    package_dir={'cloudapp': 'cloudapp'},
    description='A wrapper around CloudApp API',
    classifiers=classifiers,
    install_requires=[
        'poster==0.8.1',
        'ordereddict==1.1',
    ],
)