import setuptools
import re

__version__ = "1.1.6"


with open('log.txt', 'r') as logf:
    log = logf.read()[1:]


with open('README.md', 'r') as fh:
    long_description = fh.read().replace('<log>',
                                         log.replace('``', '"'))


setuptools.setup(
    name='colorparse',
    version=__version__,
    author='Esteban Carrillo',
    author_email='esteban.ac.naranjo@gmail.com',
    description='A string-coloring package for terminals',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tubi-carrillo/colorparse',
    py_modules=['colorparse'],
    packages=setuptools.find_packages(),
    keywords='colorparse, terminal, color, ansi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        "console_scripts": ["colorparse=colorparse:_main"],
    },
)
