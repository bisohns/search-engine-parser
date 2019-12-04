#!/bin/bash

# get current version
VERSION="$(python setup.py --version)"
echo "${VERSION}"

# install python package
pip uninstall search-engine-parser -y
pip install search-engine-parser=="${VERSION}"
python -c "import search_engine_parser"

pip uninstall search-engine-parser -y

pip install 'search-engine-parser[cli]=="${VERSION}"'

# run the cli version to get a result
python -m search_engine_parser.core.cli --engine bing search --query "Preaching to the choir" --type descriptions

# run cli with pysearch
pysearch -e youtube search -q "NoCopyrightSounds"

if [ $? -eq 0 ]; then
    echo "Package works as expected"
else
    echo "CLI handler of the package failed to execute"
    exit 1
fi
