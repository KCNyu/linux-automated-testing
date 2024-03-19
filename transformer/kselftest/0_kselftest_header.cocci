@ haskselftest @
@@
#include "../../api/kselftest_harness.h"

@ add_kselftest_harness depends on !haskselftest @
@@
#include <...>
+ #include "../../api/kselftest_harness.h"
