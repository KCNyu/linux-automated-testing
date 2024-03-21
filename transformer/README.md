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

To use the Transformer tools, follow these steps:

- Ensure you have the necessary dependencies installed, including Coccinelle.
- Navigate to the `transformer` directory and run the transformation script on your target test files.
- Verify the conversion by reviewing the transformed test files and running them within the kselftest framework.