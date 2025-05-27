#!/bin/bash

# Setup script for AirBnB console testing

echo "Setting up AirBnB Console Tests..."

# Make console executable
chmod +x console.py

# Create tests directory if it doesn't exist
mkdir -p tests

# Make test files executable
chmod +x tests/test_console_create.py
chmod +x tests/test_console_edge_cases.py

echo "Setup complete!"
echo ""
echo "To run tests:"
echo "1. Demo test: cat test_params_create | ./console.py"
echo "2. Unit tests: python3 -m unittest tests.test_console_create"
echo "3. Edge case tests: python3 -m unittest tests.test_console_edge_cases"
echo "4. All tests: python3 -m unittest discover tests"
