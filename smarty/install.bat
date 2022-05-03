@echo off
Title "PyPi in QGIS"
Echo "Adding 3rd party modules in QGIS"

REM securely download get-pip install script
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

REM install pip
python ./get-pip.py

REM install 3rd party modules
pip install --user smartystreets_python_sdk

@echo on
pause