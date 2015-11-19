#!/bin/bash

echo "Set the following environment vars:

export DYLD_FALLBACK_LIBRARY_PATH=\$DYLD_FALLBACK_LIBRARY_PATH:/usr/local/lib # For mac
export PYTHONPATH=\$PYTHONPATH:/usr/local/python_packages
export YAAFE_PATH=/usr/local/yaafe_extensions

Check by:

echo \$DYLD_FALLBACK_LIBRARY_PATH
echo \$PYTHONPATH
echo \$YAAFE_PATH
"
