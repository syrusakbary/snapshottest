all: install test

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

.PHONY: clean
clean:
	rm -rf dist/ build/

.PHONY: publish
publish: clean
	python3 setup.py sdist bdist_wheel
	python2 setup.py bdist_wheel
	twine upload dist/*
