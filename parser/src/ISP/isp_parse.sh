#!/bin/bash

LOGFILE="$1"
RESULT_FILE="result.txt"

parse_output() {
    perl -ne '
    if (m|^# selftests: (.*)$|) {
	$testdir = $1;
	$testdir =~ s|[:/]\s*|.|g;
    } elsif (m|^(?:# )*(not )?ok (?:\d+) ([^#]+)(# (SKIP)?)?|) {
        $not = $1;
        $test = $2;
        $skip = $4;
        $test =~ s|\s+$||;
        # If the test name starts with "selftests: " it is "fully qualified".
        if ($test =~ /selftests: (.*)/) {
            $test = $1;
	    $test =~ s|[:/]\s*|.|g;
        } else {
            # Otherwise, it likely needs the testdir prepended.
            $test = "$testdir.$test";
        }
        # Any appearance of the SKIP is a skip.
        if ($skip eq "SKIP") {
            $result="skip";
        } elsif ($not eq "not ") {
            $result="fail";
        } else {
            $result="pass";
        }
	print "$test $result\n";
    }
' "${LOGFILE}" >> "${RESULT_FILE}"
}

parse_output

command -v lava-test-case > /dev/null 2>&1
lava_test_case="$?"
command -v lava-test-set > /dev/null 2>&1
lava_test_set="$?"

if [ -f "${RESULT_FILE}" ]; then
    while read -r line; do
        if echo "${line}" | grep -iq -E ".* +(pass|fail|skip|unknown)$"; then
            test="$(echo "${line}" | awk '{print $1}')"
            result="$(echo "${line}" | awk '{print $2}')"

            if [ "${lava_test_case}" -eq 0 ]; then
                if [ "${result}" = "pass"  ] || [ "${result}" = "fail"  ] || [ "${result}" = "skip"  ]; then
                    test="${test/=[[:digit:]]}"
                    lava-test-case "${test}" --result "${result}"
                fi
            else
                if [ "${result}" = "pass"  ] || [ "${result}" = "fail"  ] || [ "${result}" = "skip"  ]; then
                    echo "<TEST_CASE_ID=${test} RESULT=${result}>"
                fi
            fi
        elif echo "${line}" | grep -iq -E ".*+ (pass|fail|skip|unknown)+ .*+"; then
            test="$(echo "${line}" | awk '{print $1}')"
            result="$(echo "${line}" | awk '{print $2}')"
            measurement="$(echo "${line}" | awk '{print $3}')"
            units="$(echo "${line}" | awk '{print $4}')"

            if [ "${lava_test_case}" -eq 0 ]; then
                if [ -n "${units}" ]; then
                    lava-test-case "${test}" --result "${result}" --measurement "${measurement}" --units "${units}"
                else
                    lava-test-case "${test}" --result "${result}" --measurement "${measurement}"
                fi
            else
                if [ "${result}" = "pass"  ] || [ "${result}" = "fail"  ] || [ "${result}" = "skip"  ]; then
                    echo "<TEST_CASE_ID=${test} RESULT=${result} MEASUREMENT=${measurement} UNITS=${units}>"
                fi
            fi
        elif echo "${line}" | grep -iq -E "^lava-test-set.*"; then
            test_set_status="$(echo "${line}" | awk '{print $2}')"
            test_set_name="$(echo "${line}" | awk '{print $3}')"
            if [ "${lava_test_set}" -eq 0 ]; then
                echo "case 14"
                lava-test-set "${test_set_status}" "${test_set_name}"
            else
                if [ "${test_set_status}" = "start" ]; then
                    echo "<LAVA_SIGNAL_TESTSET START ${test_set_name}>"
                else
                    echo "<LAVA_SIGNAL_TESTSET STOP>"
                fi
            fi
        fi
    done < "${RESULT_FILE}"
else
    echo "WARNING: result file is missing!"
fi
