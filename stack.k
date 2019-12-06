// Simple stack language

module STACK-SYNTAX
  imports DOMAINS-SYNTAX

  syntax Cmd ::= Int | "+" | "-" | "*" | "/" | "dup" | "drop" | "swap"
  syntax Prog ::= Cmd | Cmd Prog
endmodule

module STACK
  imports STACK-SYNTAX
  imports DOMAINS

  configuration <T> <k> $PGM:Prog </k> <stack> .List </stack> </T>

  rule C1:Cmd C2:Prog => C1 ~> C2

  rule <k> I:Int => . ... </k> <stack> .List => ListItem(I) ... </stack>

  rule <k> dup => . ... </k> <stack> ListItem(I) => ListItem(I) ListItem(I) ...</stack>
  rule <k> drop => . ... </k> <stack> ListItem(I) => .List ...</stack>
  rule <k> swap => . ... </k> <stack> ListItem(I) ListItem(J) => ListItem(J) ListItem(I) ...</stack>

  rule <k> + => . ... </k> <stack> ListItem(I) ListItem(J) => ListItem(J +Int I) .List ... </stack>
  rule <k> - => . ... </k> <stack> ListItem(I) ListItem(J) => ListItem(J -Int I) .List ... </stack>
  rule <k> * => . ... </k> <stack> ListItem(I) ListItem(J) => ListItem(J *Int I) .List ... </stack>
  rule <k> / => . ... </k> <stack> ListItem(I) ListItem(J) => ListItem(J /Int I) .List ... </stack>
endmodule
