COMPILED_RESOURCE_FILES = smarty/resources.py
RESOURCE_SRC=$(shell grep '^ *<file' smarty/resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')

.PHONY: vendor check compile install lint

install:
	pip install bandit detect-secrets flake8

lint:
	@echo "--- Flake8 ---"
	@flake8 smarty/ || true
	@echo "--- detect-secrets ---"
	@detect-secrets scan --all-files || true
	@echo "--- Bandit ---"
	bandit -r smarty/ -x ./.git

vendor:
	./vendor.sh

check:
	cd smarty && python3 -m py_compile __init__.py smarty.py smarty_dialog.py utils.py
	cd smarty && python3 -c "import sys; sys.path.insert(0, '.'); import smartystreets_python_sdk; from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder, SharedCredentials, Batch, Request; from smartystreets_python_sdk.us_street import Lookup; from smartystreets_python_sdk.us_autocomplete_pro import Lookup; print('OK')"

compile: $(COMPILED_RESOURCE_FILES)

smarty/%.py : smarty/%.qrc $(RESOURCES_SRC)
	pyrcc5 -o $*.py  $<
