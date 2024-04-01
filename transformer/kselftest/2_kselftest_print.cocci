@ haskselftest @
@@
#include "../kselftest_harness.h"

// @ print_replace depends on haskselftest @
// expression E;
// expression list Es;
// @@
// TEST(...)
// {
// <+...
// - printf(E, Es);
// + TH_LOG(E, Es);
// ...+>
// }

// @ perror_replace depends on haskselftest @
// expression E;
// expression list Es;
// @@
// TEST(...)
// {
// <+...
// - perror(E, Es);
// + TH_LOG(E, Es);
// ...+>
// }

@ fprintf_replace depends on haskselftest @
expression E = stderr, Er;
expression list Es;
@@
TEST(...)
{
<+...
- fprintf(E, Er, Es);
+ TH_LOG(Er, Es);
...+>
}