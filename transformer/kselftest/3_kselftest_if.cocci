#include "kselftest/0_kselftest_header.cocci"

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
+ ASSERT_NE(E, 0);
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
+ ASSERT_EQ(E, 0);
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
