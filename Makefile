all: install test README.rst

.PHONY: install
install:
	pip install -e ".[test]"
	pip install flake8

.PHONY: test
test:
# Run Pytest tests (including examples)
	py.test --cov=snapshottest tests examples/pytest

# Run Unittest Example
	python examples/unittest/test_demo.py

# Run nose
	nosetests examples/unittest

# Run Django Example
	cd examples/django_project && python manage.py test

.PHONY: lint
lint:
	flake8

%.rst: %.md
	pandoc $^ --from markdown --to rst -s -o $@
