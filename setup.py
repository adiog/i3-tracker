"""i3-tracker

Copyright (c) 2017 Aleksander Gajewski <adiog@brainfuck.pl>.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='i3 tracker',

    version='0.0.0',

    description='i3 tracker',
    long_description=long_description,

    url='https://github.com/adiog/i3-tracker',

    author='Aleksander Gajewski',
    author_email='adiog@quicksave.io',

    license='GPLv3',

    classifiers=[
        'Development Status:: 1 - Planning',

        'Environment :: Console',
        'Environment :: Plugins',

        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',

        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'
    ],

    keywords='i3 time tracker',

    packages=find_packages('src'),

    install_requires=['django', 'i3ipc', 'requests', 'svgwrite'],

    package_dir={
        '': 'src'
    },

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'i3-tracker-server=i3_tracker_server.manage:main'
        ],
    },
)
