#!/bin/bash

cd ..

# special make the error in map_fixed_noreplace_with_error.c:93
python3 src/main.py test/map_fixed_noreplace_with_error.c

cd -
# Define the directory to search in
SEARCH_DIR="."

# Define the old and new include paths
OLD_INCLUDE='#include "../kselftest_harness.h"'
NEW_INCLUDE='#include "../../api/src/kselftest_harness.h"'

# Find all C source files and header files in the directory and its subdirectories
find "$SEARCH_DIR" -type f \( -name "*.c" -o -name "*.h" \) -exec sed -i "s|${OLD_INCLUDE}|${NEW_INCLUDE}|g" {} +

gcc map_fixed_noreplace_with_error_transformed.c && ./a.out
