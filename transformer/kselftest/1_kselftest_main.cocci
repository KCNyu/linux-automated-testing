@ haskselftest @
@@
#include "../kselftest_harness.h"
/*  
Overly time-consuming
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
*/

@ kselftest_skip @
@@
main(...)
{
<+...
ksft_exit_skip(...);
...+>
}

@ main_as_test_without_return depends on haskselftest && !kselftest_skip @
expression ret;
@@
- int main(...)
+ TEST()
{
 ...
}
+ // TEST_HARNESS_MAIN
