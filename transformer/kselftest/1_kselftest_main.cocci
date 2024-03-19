#include "kselftest/0_kselftest_header.cocci"

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
