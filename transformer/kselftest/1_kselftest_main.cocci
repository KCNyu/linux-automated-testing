@ haskselftest @
@@
#include "../kselftest_harness.h"

@ main_as_test depends on haskselftest @
expression ret;
@@
- int main(...)
+ TEST()
{
 ...
- return ret;
+ exit(ret);
}
+ // TEST_HARNESS_MAIN

@ main_as_test_without_return depends on haskselftest @
expression ret;
@@
- int main(...)
+ TEST()
{
 ...
}
+ // TEST_HARNESS_MAIN
