#include "kselftest/0_kselftest_header.cocci"

@ argc depends on haskselftest @
@@
- argc
+ __test_global_metadata->argc

@ argv depends on haskselftest @
@@
- argv
+ __test_global_metadata->argv