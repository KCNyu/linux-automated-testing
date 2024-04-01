@ haskselftest @
@@
#include "../kselftest_harness.h"

@ main_exists @
@@
int main(...)
{
    ...
}

@ start_exists @
@@
void _start(...)
{
    ...
}

@ add_kselftest_harness depends on !haskselftest && (main_exists || start_exists) @
@@
#include <...>
+ #include "../kselftest_harness.h"
