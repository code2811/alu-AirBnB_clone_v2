#!/bin/bash


echo "Setting up AirBnB Console Tests..."


chmod +x console.py


mkdir -p tests


chmod +x tests/test_console_create.py
chmod +x tests/test_console_edge_cases.py

echo "Setup complete!"
echo ""
echo "To run tests:"
echo "1. Demo test: cat test_params_create | ./console.py"
echo "2. Unit tests: python3 -m unittest tests.test_console_create"
echo "3. Edge case tests: python3 -m unittest tests.test_console_edge_cases"
echo "4. All tests: python3 -m unittest discover tests"
