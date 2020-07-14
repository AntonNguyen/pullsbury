.PHONY: install dev-install lint test .pipenv-installed

PYTHON?=python
PIP=$(PYTHON) -m pip
PIPENV=$(PYTHON) -m pipenv
NOSETESTS=$(PIPENV) run nosetests
COVERAGE=$(PIPENV) run coverage
FLAKE8=$(PYTHON) -m flake8 --ignore E501

APP_VERSION?=0.0.0

.pipenv-installed:
	$(PIPENV) --version || $(PIP) install pipenv

install: .pipenv-installed
	$(PIPENV) install

dev-install: install
	$(PIPENV) install --dev

lint: dev-install
	$(FLAKE8)

test: dev-install
	$(NOSETESTS) --with-coverage --cover-xml
	$(COVERAGE) xml

build:
	@docker build \
		--build-arg ARTIFACTORY_CREDENTIALS_USR=${ARTIFACTORY_CREDENTIALS_USR} \
		--build-arg ARTIFACTORY_CREDENTIALS_PSW=${ARTIFACTORY_CREDENTIALS_PSW} \
		-t gcr.io/freshbooks-builds/pullsbury-gitboy:$(APP_VERSION) \
		.
