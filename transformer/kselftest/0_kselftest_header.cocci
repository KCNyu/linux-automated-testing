@ haskselftest @
@@
#include "../kselftest_harness.h"

@ add_kselftest_harness depends on !haskselftest @
@@
#include <...>
+ #include "../kselftest_harness.h"
