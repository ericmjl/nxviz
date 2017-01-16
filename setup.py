from nxviz import __version__, __email__, __author__
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'cryptography',
    'hypothesis',
    'matplotlib',
    'networkx',
    'numpy',
    'palettable',
    'pandas',
    'pytest',
    'polcart',
]

setup(
    name='nxviz',
    version=__version__,
    description="Graph Visualization Package",
    long_description=readme + '\n\n' + history,
    author=__author__,
    author_email=__email__,
    url='https://github.com/ericmjl/nxviz',
    packages=[
        'nxviz',
    ],
    package_dir={'nxviz': 'nxviz'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    keywords='nxviz',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
