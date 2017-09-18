from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []
with open('requirements.txt') as rqmts:
    for r in rqmts:
        requirements.append(r.strip('\n'))

setup(
    name='nxviz',
    version="0.3.2",
    description="Graph Visualization Package",
    long_description=readme + '\n\n' + history,
    author="Eric J. Ma",
    author_email="ericmajinglong@gmail.com",
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
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
