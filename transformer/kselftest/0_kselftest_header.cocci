@ haskselftest @
@@
#include "../kselftest_harness.h"

@ main_exists @
@@
int main(...)
{
    ...
}

@ add_kselftest_harness depends on !haskselftest && main_exists @
@@
#include <...>
+ #include "../kselftest_harness.h"
