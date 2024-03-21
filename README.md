# linux-automated-testing

> 🌐 **Languages:** [English](./README.md) | [Русский](./README_ru.md)

![framework](./framework.png) 
This project focuses on enhancing the Linux kernel selftest framework by introducing significant improvements across its `api`, `transformer`, and `parser` components. These enhancements aim to streamline the process of writing, managing, and interpreting kernel self-tests, making the framework more efficient and user-friendly.

## Project Components

### [API](./api/README.md)

The `api` component updates the Linux kernel selftests framework, introducing new global metadata for test information, filtering capabilities at various levels, and an improved output format. It addresses issues such as infinite loops in `FIXTURE_TEARDOWN` and enables both CLI and GUI options for test selection.

### [Transformer](./transformer/README.md)

The `transformer` addresses historical inconsistencies in test output formats by converting traditional test files into ones that utilize the kselftest framework. It automates this process using Coccinelle semantic patching and Python scripts, enhancing the manageability of test cases.

### [Parser](./parser/README.md)

The `parser` component is designed to parse the results logs from Kselftest runs, preparing them for submission to CI systems. It compares three versions of the Parser, highlighting the current implementation's efficiency and optimization in parsing and submitting test results.
