COMPILED_RESOURCE_FILES = resources.py
RESOURCE_SRC=$(shell grep '^ *<file' resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')

.PHONY: vendor check compile

vendor:
	cd .. && ./vendor.sh

check:
	python3 -m py_compile __init__.py smarty.py smarty_dialog.py utils.py
	python3 -c "import sys; sys.path.insert(0, '.'); import smartystreets_python_sdk; from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder, SharedCredentials, Batch, Request; from smartystreets_python_sdk.us_street import Lookup; from smartystreets_python_sdk.us_autocomplete_pro import Lookup; print('OK')"

compile: $(COMPILED_RESOURCE_FILES)

%.py : %.qrc $(RESOURCES_SRC)
	pyrcc5 -o $*.py  $<
