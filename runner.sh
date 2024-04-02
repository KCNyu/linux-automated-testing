#!/bin/bash

# Define directories and log file path
WORKSPACE="WORKSPACE"
ORIGIN_DIR="stable-linux-5.10.y"
TEST_DIR="linux-5.10.y"
LOG_DIR="log"
TRANSFORMER_DIR=transformer

# Ensure a TARGETS argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <TARGETS>"
    exit 1
fi

# Function to download and extract Linux kernel if it doesn't exist
download_and_extract_kernel() {
    if [ ! -d "$ORIGIN_DIR" ]; then
        echo "Directory $ORIGIN_DIR does not exist, starting download..."
        wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.10.213.tar.xz >/dev/null 2>&1
        mkdir -p "$ORIGIN_DIR"
        tar -xvf linux-5.10.213.tar.xz -C "$ORIGIN_DIR" --strip-components=1 >/dev/null 2>&1

        if [ $? -eq 0 ]; then
            echo "Download and extraction successful."
        else
            echo "Error downloading and extracting the kernel. Please check the paths and permissions."
            exit 1
        fi
    else
        echo "Directory $ORIGIN_DIR already exists, skipping download."
    fi
}

# Function to remove the test directory if it exists
remove_test_dir() {
    if [ -d "$TEST_DIR" ]; then
        echo "Directory $TEST_DIR already exists, starting removal..."
        sudo rm -rf "$TEST_DIR"
    fi
}

# Function to copy the origin directory to test directory
copy_to_test_dir() {
    if [ ! -d "$TEST_DIR" ]; then
        echo "Starting to copy $ORIGIN_DIR to $TEST_DIR..."
        cp -r "$ORIGIN_DIR" "$TEST_DIR"
    fi
}

# Function to create log directory if it doesn't exist
create_log_dir() {
    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR"
    fi
}

# Additional step: Copy a specific file if conditions are met and then rename it
copy_specific_file_for_test() {
    if [ "$1" == "tmpfs" ]; then
        local tmpfs_dir="$ORIGIN_DIR/tools/testing/selftests/tmpfs"
        local src_file="../$TRANSFORMER_DIR/test/bug-link-o-tmpfile_with_error.c"
        local dest_file="$tmpfs_dir/bug-link-o-tmpfile_with_error.c"
        local final_file="$tmpfs_dir/bug-link-o-tmpfile.c"
        echo "Copying specific test file for tmpfs..."
        # Copy the file
        if cp "$src_file" "$dest_file"; then
            # If copy succeeds, rename the file
            mv "$dest_file" "$final_file"
            echo "File copied and renamed successfully."
        else
            echo "Error copying file. Please check the paths and permissions."
            exit 1
        fi
    elif [ "$1" == "vm" ]; then
        local vm_dir="$ORIGIN_DIR/tools/testing/selftests/vm"
        local src_file="../$TRANSFORMER_DIR/test/map_hugetlb_with_error.c"
        local dest_file="$vm_dir/map_hugetlb_with_error.c"
        local final_file="$vm_dir/map_hugetlb.c"
        echo "Copying specific test file for vm..."
        # Copy the file
        if cp "$src_file" "$dest_file"; then
            # If copy succeeds, rename the file
            mv "$dest_file" "$final_file"
            echo "File copied and renamed successfully."
        else
            echo "Error copying file. Please check the paths and permissions."
            exit 1
        fi
    fi
}

# Main script execution starts here

# Ensure workspace directory exists
if [ ! -d "$WORKSPACE" ]; then
    mkdir -p "$WORKSPACE"
fi

cd "$WORKSPACE"

# Download and extract kernel
download_and_extract_kernel

# Remove and prepare test directory
remove_test_dir

# Copy specific file if runner.sh exists and test is tmpfs
copy_specific_file_for_test "$1"

copy_to_test_dir

# Create log directory
create_log_dir

# Run tests before transformation
cd "$ORIGIN_DIR"
sudo make -C tools/testing/selftests TARGETS="$1" run_tests | tee "../$LOG_DIR/${1}_before.log"

# Execute transformation
cd ../../transformer
echo "Current directory: $(pwd)"
bash run.sh "$1"

# Run tests after transformation
cd "../$WORKSPACE/$TEST_DIR"
sudo make -C tools/testing/selftests TARGETS="$1" run_tests | tee "../$LOG_DIR/${1}_after.log"

# Parse logs
cd ../../parser
./src/parse.pl -i "../$WORKSPACE/$LOG_DIR/${1}_before.log"
./src/parse.pl -i "../$WORKSPACE/$LOG_DIR/${1}_after.log" -j
