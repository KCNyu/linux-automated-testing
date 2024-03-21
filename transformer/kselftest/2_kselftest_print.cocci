@ haskselftest @
@@
#include "../kselftest_harness.h"

@ print_replace depends on haskselftest @
expression E;
expression list Es;
@@
TEST(...)
{
<+...
- printf(E, Es);
+ TH_LOG(E, Es);
...+>
}

@ perror_replace depends on haskselftest @
expression E;
expression list Es;
@@
TEST(...)
{
<+...
- perror(E, Es);
+ TH_LOG(E, Es);
...+>
}
