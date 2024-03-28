@ haskselftest @
@@
#include "../kselftest_harness.h"

/* following if statements with return/exit are replaced by ASSERT_* */

@ if_eq depends on haskselftest @
expression E1, E2;
expression ret != 0;
@@
TEST(...){
<+...
- if(E1 == E2)
+ ASSERT_NE(E1, E2);
{
...
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
}
...+>
}

/////////////////////////////////////////

@ if_ne depends on haskselftest @
expression E1, E2;
expression ret != 0;
@@
TEST(...){
<+...
- if(E1 != E2)
+ ASSERT_EQ(E1, E2);
{
...
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
}
...+>
}

/////////////////////////////////////////

@ if_le depends on haskselftest @
expression E1, E2;
expression ret != 0;
@@
TEST(...){
<+...
- if(E1 < E2)
+ ASSERT_GE(E1, E2);
{
...
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
}
...+>
}

/////////////////////////////////////////

@ if_ge depends on haskselftest @
expression E1, E2;
expression ret != 0;
@@
TEST(...){
<+...
- if(E1 > E2)
+ ASSERT_LE(E1, E2);
{
...
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
}
...+>
}

/////////////////////////////////////////

/* this rule should be applied before the next one due to !E will be think as E  */

@ single_if_ne depends on haskselftest @
expression E;
expression ret != 0;
@@
TEST(...){
<+...
- if(!E)
+ ASSERT_TRUE(E);
{
...
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
}
...+>
}

/////////////////////////////////////////

@ single_if_eq depends on haskselftest @
expression E;
expression ret != 0;
@@
TEST(...){
<+...
- if(E)
+ ASSERT_FALSE(E);
{
...
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
}
...+>
}

/////////////////////////////////////////

@ if_eq_without_braces depends on haskselftest @
expression E1, E2;
expression ret != 0;
@@
TEST(...){
<+...
- if(E1 == E2)
+ ASSERT_NE(E1, E2); // {
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
+ // }
...+>
}

/////////////////////////////////////////

@ if_ne_without_braces depends on haskselftest @
expression E1, E2;
expression ret != 0;
@@
TEST(...){
<+...
- if(E1 != E2)
+ ASSERT_EQ(E1, E2); // {
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
+ // }
...+>
}

/////////////////////////////////////////

@ if_le_without_braces depends on haskselftest @
expression E1, E2;
expression ret != 0;
@@
TEST(...){
<+...
- if(E1 < E2)
+ ASSERT_GE(E1, E2); // {
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
+ // }
...+>
}

/////////////////////////////////////////

@ if_ge_without_braces depends on haskselftest @
expression E1, E2;
expression ret != 0;
@@
TEST(...){
<+...
- if(E1 > E2)
+ ASSERT_LE(E1, E2); // {
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
+ // }
...+>
}

/////////////////////////////////////////

@ ingle_if_ne_without_braces depends on haskselftest @
expression E;
expression ret != 0;
@@
TEST(...){
<+...
- if(!E)
+ ASSERT_TRUE(E); // {
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
+ // }
...+>
}

/////////////////////////////////////////

@ ingle_if_eq_without_braces depends on haskselftest @
expression E;
expression ret != 0;
@@
TEST(...){
<+...
- if(E)
+ ASSERT_FALSE(E); // {
(
- return ret;
| 
- exit(ret);
)
+ exit(ret);
+ // }
...+>
}