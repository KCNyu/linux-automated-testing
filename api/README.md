# API Directory Overview

> 🌐 **Languages:** [English](./README.md) | [Русский](./README_ru.md)

The `api` directory contains the source code and tests for enhancements made to the Linux kernel self-tests framework. These enhancements aim to improve the flexibility, usability, and effectiveness of kernel self-tests by introducing new features such as global metadata, filtering options, and improved output formats.

## Key Features

1. **Global Metadata Addition:** Allows for the supplementation of test information and the addition of necessary extra variables.

2. **Filtering Capabilities:**
   - Implements filters at the Fixture, Test, and Variant levels.
   - While it's not possible to select an exact combination of fixture, variant, and test, users can combine fixtures and tests.
   - Features both command-line and GUI options for test selection.

3. **Improved Output Format:** Updates the test output format to be more visually informative.

4. **Bug Fixes:**
   - Addresses and fixes the issue where the use of `ASSERT_*` in `FIXTURE_TEARDOWN` could lead to infinite loops.

## Getting Started

To use the enhancements in the `api` directory, follow these steps:

1. **Installation:** Ensure that your environment is set up with the necessary dependencies for Linux kernel self-tests.

2. **Running Tests:** Use the provided command-line or GUI tools to select and run your tests. When compiling for GUI usage, ensure to include the `-DGUI` and `-lncurses` flags to enable GUI features and dependencies. Filters can be applied to customize the testing scope, allowing for a more targeted test execution.


3. **Reviewing Results:** Examine the output provided by the tests for insights and potential issues highlighted by the enhanced formats.