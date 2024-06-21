# Compiler
> This project was developed with the assistance of ChatGPT to help understand the process of building a compiler.

This project involves building a simple compiler to parse and interpret a subset of a programming language.
To compile the source code:
1. First open the terminal in Makefile
2. Type mingw32-make
3. Run the compiler with the test file ./compiler test/do.c

### Dowhile Code Ex that was used:
```
x = 1;
do {
    x = x + 1;
} while (i < 10);
```

### Syntax

```
PROG = STMTS
BLOCK = { STMTS }
STMTS = STMT*
WHILE = while (E) STMT
DO = do STMT while (E)
ASSIGN = id '=' E;
E = F (op E)*
F = (E) | Number | Id
```

### Results of Lexical, Token Dump and Parsing

```PS C:\CSIE\SEM 4\System Programming\sp\Week 2> mingw32-make
>>
gcc -std=c99 -O0 lexer.c compiler.c main.c -o compiler
PS C:\CSIE\SEM 4\System Programming\sp\Week 2> ./compiler test/do.c
x = 1;
do{
x = x + 1;
}
while(i<10);

========== lex ==============      
token=x
token==
token=1
token=;
token=do
token={
token=x
token==
token=x
token=+
token=1
token=;
token=}
token=while
token=(
token=i
token=<
token=10
token=)
token=;
========== dump ==============     
0:x
1:=
2:1
3:;
4:do
5:{
6:x
7:=
8:x
9:+
10:1
11:;
12:}
13:while
14:(
15:i
16:<
17:10
18:)
19:;
============ parse =============   
t0 = 1
x = t0
(L0)
t1 = x
t2 = 1
t3 = t1 + t2
x = t3
(L1)
t4 = i
t5 = 10
t6 = t4 < t5
if not T6 goto L2
goto L0
(L2)
``` 