#include "kselftest/0_kselftest_header.cocci"

@ print_replace @
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
