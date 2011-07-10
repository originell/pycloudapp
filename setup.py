import os
from distutils.core import setup

VERSION = '0.1'

classifiers = [
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Environment :: Web Environment",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Development Status :: 5 - Production/Stable",
]

setup(
    name='pycloudapp',
    version=VERSION,
    url='https://github.com/originell/pycloudapp',
    author='Luis Nell',
    author_email = 'cooperate@originell.org',
    packages=['cloudapp'],
    package_dir={'cloudapp': 'cloudapp'},
    description='A wrapper around the CloudApp API',
    long_description="""\
PyCloudApp API
--------------

PyCloudApp is a wrapper around the CloudApp API.

It supports the following CloudApp API Features:

    - Authenticate a user
    - Getting Infos from a cl.ly URL
    - List a user's items
    - Create Bookmarks
    - Upload Files

For full functionality you need to have *poster* as well as
Python 2.7 or *ordereddict* installed.

Note that the CloudApp API has been extended a **lot**, feel free
to fork and contribute to the project on GitHub.
""",
    classifiers=classifiers,
    install_requires=[
        'poster==0.8.1',
        'ordereddict==1.1',
    ],
)
