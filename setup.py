# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

tests_require = [
    'six',
    'pytest>=3.0',
    'pytest-cov',
    'nose',
]

setup(
    name='snapshottest',
    version='0.4.0',
    description='Snapshot Testing utils for Python',
    long_description=readme,
    author='Syrus Akbary',
    author_email='me@syrusakbary.com',
    url='https://github.com/syrusakbary/snapshottest',
    # custom PyPI classifier for pytest plugins
    entry_points = {
        'pytest11': [
            'snapshottest = snapshottest.pytest',
        ],
        'nose.plugins.0.10': [
            'snapshottest = snapshottest.nose:SnapshotTestPlugin'
        ]
    },
    install_requires=[
        'six>=1.10.0',
        'termcolor',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'pytest': [
            'pytest',
        ],
        'nose': [
            'nose',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
    ],
    license='MIT',
    packages=find_packages(exclude=('tests',))
)
