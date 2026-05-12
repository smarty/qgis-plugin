COMPILED_RESOURCE_FILES = smarty/resources.py
RESOURCE_SRC=$(shell grep '^ *<file' smarty/resources.qrc | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')

QGIS_PLUGINS_DIR = $(HOME)/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins

.PHONY: vendor check compile install lint deploy redeploy

install:
	pip install bandit detect-secrets flake8

lint:
	@echo "--- Flake8 ---"
	@flake8 smarty/ --exclude=smarty/smartystreets_python_sdk,smarty/smartystreets_python_sdk-6.1.0.dist-info || true
	@echo "--- detect-secrets ---"
	@detect-secrets scan --all-files || true
	@echo "--- Bandit ---"
	bandit -r smarty/ -x smarty/smartystreets_python_sdk,smarty/test,./.git

deploy:
	rm -rf "$(QGIS_PLUGINS_DIR)/smarty"
	cp -rf smarty "$(QGIS_PLUGINS_DIR)/smarty"

redeploy: deploy
	killall QGIS > /dev/null 2>&1
	open -a QGIS

vendor:
	./vendor.sh

check:
	cd smarty && python3 -m py_compile __init__.py smarty.py smarty_dialog.py utils.py
	cd smarty && python3 -c "import sys; sys.path.insert(0, '.'); import smartystreets_python_sdk; from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder, SharedCredentials, Batch, Request; from smartystreets_python_sdk.us_street import Lookup; from smartystreets_python_sdk.us_autocomplete_pro import Lookup; print('OK')"

compile: $(COMPILED_RESOURCE_FILES)

smarty/%.py : smarty/%.qrc $(RESOURCES_SRC)
	pyrcc5 -o $*.py  $<
