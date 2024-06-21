# Intepreter of BASIC with Python
>參考 https://ruslanspivak.com/lsbasi-part1/
https://www.youtube.com/watch?v=YYvBy0vqcSw&list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD&index=3&ab_channel=CodePulse 
Watched and understand, when it start doing other mathematical expressions, I tried writing it by myself. The other things was done by looking and understanding what the person in the video was doing.

## Explanation

The program evaluates simple arithmetic expression language. It reads, parses and evaluates expression. It is not a full compiler but it has the process of tokenizing, parsing and evaluating expressions!

## What I studied by Watching the vid:
- Lexical Analysis   
 Convert raw text input into tokens.

- Syntax Analysis (Parsing)   
 Convert tokens into an Abstract Syntax Tree (AST).

- Interpretation   
 Evaluate the AST to compute the result of expressions.

- Error Handling   
 Provide feedback if error was encountered.


## Results
By running shell.py you can try and run the results as below:
- Make a math expression and got an error when divided by zero.
```
Program > 8/0
Traceback (most recent call last): 
File <stdin>, line 1, in <program> 
Runtime Error: Division by zero    

8/0
  ^
```
- Make a mathematical expression and got an error if it's not a number
```
Program > 30+a
Illegal Character: 'a'
File <stdin>, line 1

30+a
   ^
```
- simple mathematics
```
Program > 3+5*(10-4)
33
Program > 7/2
3.5
```