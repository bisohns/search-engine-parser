#!/bin/bash

# install python package
pip install search-engine-parser

# run the cli version to get a result
python -m search_engine_parser.core.cli --query "Preaching to the choir" --engine bing --type descriptions --rank 1

if [ $? -eq 0 ]; then
    echo "Package works as expected"
else
    echo "CLI handler of the package failed to execute"
fi