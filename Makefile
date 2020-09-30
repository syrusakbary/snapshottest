all: install test

.PHONY: develop
develop: install install-tools

.PHONY: install
install:
	pip install -e ".[test]"

.PHONY: install-tools
install-tools:
	pip install flake8 black==20.8b1

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

.PHONY: format
format:
	black --check setup.py snapshottest tests examples --exclude 'snapshots\/snap_.*.py$$'

.PHONY: format-fix
format-fix:
	black setup.py snapshottest tests examples --exclude 'snapshots\/snap_.*.py$$'

.PHONY: clean
clean:
	rm -rf dist/ build/

.PHONY: publish
publish: clean
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
