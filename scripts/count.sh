#!/bin/bash

TARGET_DIR="../WORKSPACE/stable-linux-5.10.y/tools/testing/selftests"
echo "Target,SH Files,C Files with main/_start,C Files with kselftest.h,C Files with kselftest_harness.h" > ./test_counts.csv

TARGETS=(android arm64 bpf breakpoints capabilities cgroup clone3 core cpufreq cpu-hotplug drivers/dma-buf efivarfs exec filesystems filesystems/binderfs filesystems/epoll firmware fpu ftrace futex gpio intel_pstate ipc ir kcmp kexec kvm lib livepatch lkdtm membarrier memfd memory-hotplug mincore mount mqueue net net/forwarding net/mptcp netfilter nsfs pidfd pid_namespace powerpc proc pstore ptrace openat2 rseq rtc seccomp sigaltstack size sparc64 splice static_keys sync sysctl tc-testing timens timers tmpfs tpm2 user vm x86 zram)

# 初始化总计数器
total_sh_files=0
total_main_start_files=0
total_kselftest_files=0
total_kselftest_harness_files=0

for TARGET in "${TARGETS[@]}"; do
    sh_files=0
    main_start_files=0
    kselftest_files=0
    kselftest_harness_files=0

    while IFS= read -r file; do
        if [[ "$file" =~ \.sh$ ]]; then
            ((sh_files++))
        elif [[ "$file" =~ \.c$ ]]; then
            if grep -qE "int main|void _start" "$file"; then
                ((main_start_files++))
            fi
            if grep -qE "#include \".*kselftest_harness.h\"" "$file"; then
                ((kselftest_harness_files++))
                ((main_start_files++))
                continue
            fi
            if grep -qE "#include \".*kselftest.h\"" "$file"; then
                ((kselftest_files++))
            fi
        fi
    done < <(find "$TARGET_DIR/$TARGET" -type f \( -name "*.c" -o -name "*.sh" \))

    # 更新总计
    ((total_sh_files+=sh_files))
    ((total_main_start_files+=main_start_files))
    ((total_kselftest_files+=kselftest_files))
    ((total_kselftest_harness_files+=kselftest_harness_files))

    echo "$TARGET,$sh_files,$main_start_files,$kselftest_files,$kselftest_harness_files" >> ./test_counts.csv
done

# 添加总计到CSV
echo "Total,$total_sh_files,$total_main_start_files,$total_kselftest_files,$total_kselftest_harness_files" >> ./test_counts.csv

echo "CSV file created at ./test_counts.csv"
