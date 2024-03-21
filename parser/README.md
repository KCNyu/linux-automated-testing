# Parser Directory Overview

The `parser` directory is dedicated to parsing the run results logs from Kselftests and preparing them for submission to CI systems. This directory lists three versions of the Parser, comparing their efficiency and optimization highlights.

> 🌐 **Languages:** [English](./README.md) | [Русский](./README_ru.md)

## Parser Versions

### ISP RAS Version

- **Base:** Builds on the older version implemented by Linaro, using Perl and shell scripts. It parses the logs line-by-line using Perl, stores the parsed results in a CSV-like format, and then submits them to LAVA using shell scripts.
- **Drawbacks:**
  1. Lower runtime efficiency and slow parsing speed.
  2. Unable to parse sub-tests.

### Linaro Version

- **Implementation:** Utilizes Python for the Parser part, storing parsed results in a CSV-like format and submitting them to LAVA using shell scripts.
- **Drawbacks:**
  1. Although it supports parsing sub-tests, the naming format is not uniformly encapsulated.
  2. Lacks support for saving parsed errors.

### Current Implementation

- **Technology:** Fully implemented in Perl without external dependencies, integrating both the Parser and Submitter parts. Submissions to LAVA are made using in-memory arrays, significantly improving submission efficiency.
- **Advantages:**
  1. Increased parsing and submission rates.
  2. Supports more granular parsing of sub-tests with unified naming.
  3. Allows submission of tests from the same subsystem as a SET, facilitating test management.
  4. Supports output of error reasons.
  5. Capable of saving parsed results in both JSON and CSV formats, enabling easy interfacing with other CI systems through corresponding submitter implementations.

## Getting Started

To utilize the parsers, navigate to the respective version's directory and follow the specific instructions provided within each. The choice of parser version may depend on your specific requirements for efficiency, error handling, and the format of submissions to CI systems.
