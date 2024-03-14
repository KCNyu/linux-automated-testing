@rule_if_eq_with_return@
expression E1, E2;
@@
main(...){
<+...
- if(E1 == E2)
+ ASSERT_NE(E1, E2);
{
...
(
- return 1;
| 
- exit(1);
)
+ exit(1);
}
...+>
}
/////////////////////////////////////////
@rule_if_ne_with_return@
expression E1, E2;
@@
main(...){
<+...
- if(E1 == E2)
+ ASSERT_EQ(E1, E2);
{
...
(
- return 1;
| 
- exit(1);
)
}
...+>
}
/////////////////////////////////////////

@rule_single_if@
expression E, ret;
@@
main(...){
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
/////////////////////////////////////////

@rule_single_if_neg@
expression E, ret;
@@
main(...){
<+...
- if(!E)
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
///////////////////////////////////////
@rule_replace_printf_to_log@
expression E;
@@
main(...){
<+...
- printf(E);
+ TH_LOG(E);
...+>
}

///////////////////////////////////////
@rule_replace_perror_to_log@
expression E;
@@
main(...){
<+...
- perror(E);
+ TH_LOG(E);
...+>
}
/////////////////////////////////////////

@rule_replace_main@
expression E, ret;
@@
- int main(...)
+ TEST()
{
 ... 
}

/////////////////////////////////////////
@rule_add_test_main@
@@
TEST()
{
    ...
}
+ // TEST_HARNESS_MAIN
