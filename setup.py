# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

tests_require = ["pytest>=4.6", "pytest-cov", "nose", "django>=1.10.6"]

setup(
    name="snapshottest",
    version="1.0.0a0",
    description="Snapshot testing for pytest, unittest, Django, and Nose",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Syrus Akbary",
    author_email="me@syrusakbary.com",
    url="https://github.com/syrusakbary/snapshottest",
    # custom PyPI classifier for pytest plugins
    entry_points={
        "pytest11": [
            "snapshottest = snapshottest.pytest",
        ],
        "nose.plugins.0.10": ["snapshottest = snapshottest.nose:SnapshotTestPlugin"],
    },
    install_requires=["termcolor", "fastdiff>=0.1.4,<1"],
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
        "pytest": [
            "pytest",
        ],
        "nose": [
            "nose",
        ],
    },
    requires_python=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Unit",
    ],
    license="MIT",
    packages=find_packages(exclude=("tests",)),
)
