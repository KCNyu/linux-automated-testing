#!/bin/bash

# Ensure a test directory is specified
if [ $# -ne 1 ]; then
    echo "Usage: $0 <TEST_DIRECTORY_NAME>"
    exit 1
fi

# Define the workspace and target directories
WORKSPACE_DIR="../WORKSPACE"
TESTS_DIR="$WORKSPACE_DIR/linux-5.10.y/tools/testing/selftests/$1"

# Check if the test directory exists
if [ ! -d "$TESTS_DIR" ]; then
    echo "The specified directory does not exist: $TESTS_DIR"
    exit 2
fi

# Process each file in the test directory
echo "Processing files in $TESTS_DIR"
for FILE in "$TESTS_DIR"/*; do
    if [ -f "$FILE" ]; then
        # Run the Python script on each file
        python3 src/main.py "$FILE" --in-place
    fi
done

# Copy necessary header files
echo "Copying header files to $TESTS_DIR"
HEADER_FILES=(kselftest_harness.h kselftest.h)
for HEADER_FILE in "${HEADER_FILES[@]}"; do
    cp "../api/src/$HEADER_FILE" "$WORKSPACE_DIR/linux-5.10.y/tools/testing/selftests/"
done

echo "Completed processing."
