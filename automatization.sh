#!/bin/bash

echo "Getting python3 executable location"
python_exec_loc=$(which python3)
if [ $? -eq 0 ]; then echo "OK"; else echo "Problem getting python3 executable location"; exit 1; fi
echo "$python_exec_loc"
echo "------------------------------------------------"

echo "Running config tests"
$python_exec_loc test_config.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Configuration test failed"; exit 1; fi
echo "------------------------------------------------"

echo "Running worker tests"
$python_exec_loc test_worker.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Worker test failed"; exit 1; fi
echo "------------------------------------------------"

echo "Running test on files"
$python_exec_loc test_files.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Test on files failed"; exit 1; fi
echo "------------------------------------------------"

echo "ALL SET UP!"
echo "to start the program, execute:"
echo "$python_exec_loc naked.py"
