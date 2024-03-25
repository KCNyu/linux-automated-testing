# Transformer Directory Overview

> 🌐 **Languages:** [English](./README.md) | [Русский](./README_ru.md)

The `transformer` directory houses the tools and scripts designed to address the historical inconsistency in the output formats of Linux kernel self-tests. With less than 20% of tests using the kselftest framework, managing and interpreting test results has been challenging. The Transformer aims to standardize test files by converting those not using the kselftest framework into a unified format.

## How It Works

The transformation process involves several key steps, leveraging Coccinelle semantic patching and Python scripts to automate the conversion:

1. **Adding Dependency:** Automatically adds a relative path dependency to `kselftest_harness.h` to the test files.

2. **Dependency Check:** Utilizes Spatch to verify the successful addition of the dependency.

3. **Test Function Transformation:** Converts main test functions into tests encapsulated by the TEST macro definition.

4. **Standardizing External Output APIs:** Changes external output APIs (such as `printf`, `perror`, etc.) to the unified `ksft_print_msg` framework output API.

5. **Standardizing Internal Output APIs:** Modifies internal output APIs within the test to use the unified `TH_LOG`/`LOG` framework output APIs.

6. **Conditional Test Handling:** Transforms specific conditional tests into corresponding `EXPECT_*` or `ASSERT_*` cases and packages the appropriate cleanup functions.

7. **Exit Value Replacement:** Replaces exit values with framework-specific macro exit values (`KSFT_PASS`, `KSFT_FAIL`, etc.).

8. **Command-Line Arguments Conversion:** Transforms command-line dependent variables (`argc`, `argv`, etc.) into `__test_global_metadata`, facilitating features like filtering without requiring changes to external script execution.

## Getting Started

- **Prepare Environment:** Ensure all necessary dependencies are installed on your system. This includes having Coccinelle, which is crucial for the semantic patching process.
  
- **Navigate to Transformer:** Change your current working directory to the `transformer` directory. This step is imperative as the transformation script needs to be executed from within this directory to correctly access and apply the transformation rules and dependencies:

  ```bash
  cd path/to/transformer
  ```

- **Execute Transformation:** Once in the transformer directory, initiate the transformation process by running the transformation script on your target test files. It is important to maintain the directory context to ensure paths and dependencies are correctly resolved:

  ```bash
  python3 src/main.py <file>
  ```

  Replace `<file>` with the path to the test file you wish to transform. Note: Ensure the path is relative to the transformer directory or provide an absolute path to the test file.

- **Verify Conversion:** After running the script, review the transformed test files to ensure the conversion aligns with the expected outcomes. Subsequently, execute the modified tests within the kselftest framework to confirm their functionality and adherence to the standardized format.
