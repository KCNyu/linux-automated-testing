@ haskselftest @
@@
#include "../kselftest_harness.h"

/* following if statements with return/exit are replaced by ASSERT_* */

@ if_eq depends on haskselftest @
expression E1, E2, E3;
identifier T;
@@
TEST(...){
<+...
- E1 = E3; 
- if(E1 == E2)
+ ASSERT_NE(E3, E2);
{
...
- goto T;
}
...+>
}

/////////////////////////////////////////

@ if_ne depends on haskselftest @
expression E1, E2, E3;
identifier T;
@@
TEST(...){
<+...
- E1 = E3; 
- if(E1 != E2)
+ ASSERT_EQ(E3, E2);
{
...
- goto T;
}
...+>
}

/////////////////////////////////////////

@ if_le depends on haskselftest @
expression E1, E2, E3;
identifier T;
@@
TEST(...){
<+...
- E1 = E3; 
- if(E1 < E2)
+ ASSERT_GE(E3, E2);
{
...
- goto T;
}
...+>
}

/////////////////////////////////////////

@ if_ge depends on haskselftest @
expression E1, E2, E3;
identifier T;
@@
TEST(...){
<+...
- E1 = E3; 
- if(E1 > E2)
+ ASSERT_LE(E3, E2);
{
...
- goto T;
}
...+>
}

/////////////////////////////////////////

/* this rule should be applied before the next one due to !E will be think as E  */

@ single_if_ne depends on haskselftest @
expression E;
identifier T;
@@
TEST(...){
<+...
- if(!E)
+ ASSERT_TRUE(E);
{
...
- goto T;
}
...+>
}

/////////////////////////////////////////

@ single_if_eq depends on haskselftest @
expression E;
identifier T;
@@
TEST(...){
<+...
- if(E)
+ ASSERT_FALSE(E);
{
...
- goto T;
}
...+>
}

/////////////////////////////////////////

@ if_eq_without_braces depends on haskselftest @
expression E1, E2, E3;
identifier T;
@@
TEST(...){
<+...
- E1 = E3; 
- if(E1 == E2)
+ ASSERT_NE(E3, E2); // {
- goto T;
+ // }
...+>
}

/////////////////////////////////////////

@ if_ne_without_braces depends on haskselftest @
expression E1, E2, E3;
identifier T;
@@
TEST(...){
<+...
- E1 = E3; 
- if(E1 != E2)
+ ASSERT_EQ(E3, E2); // {
- goto T;
+ // }
...+>
}

/////////////////////////////////////////

@ if_le_without_braces depends on haskselftest @
expression E1, E2, E3;
identifier T;
@@
TEST(...){
<+...
- E1 = E3; 
- if(E1 < E2)
+ ASSERT_GE(E3, E2); // {
- goto T;
+ // }
...+>
}

/////////////////////////////////////////

@ if_ge_without_braces depends on haskselftest @
expression E1, E2, E3;
identifier T;
@@
TEST(...){
<+...
- E1 = E3; 
- if(E1 > E2)
+ ASSERT_LE(E3, E2); // {
- goto T;
+ // }
...+>
}

/////////////////////////////////////////

@ ingle_if_ne_without_braces depends on haskselftest @
expression E;
identifier T;
@@
TEST(...){
<+...
- if(!E)
+ ASSERT_TRUE(E); // {
- goto T;
+ // }
...+>
}

/////////////////////////////////////////

@ ingle_if_eq_without_braces depends on haskselftest @
expression E;
identifier T;
@@
TEST(...){
<+...
- if(E)
+ ASSERT_FALSE(E); // {
- goto T;
+ // }
...+>
}
