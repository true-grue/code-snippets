// code from https://github.com/litwr2/simple-rdc
// modified for use of precedence climbing

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <stack>
#define MAXSIZE 10000000
using namespace std;

char *infix, *postfix;
char s[MAXSIZE], r[MAXSIZE];
void Term(), Element(), Component(), Item();

void error(unsigned n) {
  cerr << "Error!\n";
  exit(n);
}
int Prec(char op) {
  switch (op) {
    case '+':
    case '-':
      return 10;
    case '*':
    case '/':
      return 20;
    case '^':
      return 30;
    default:
      return -1;
  }
}
void Formula(int prec) {
  int op, pr;
  Component();
  while ((pr = Prec(*infix)) >= prec) {
    op = *infix++;
    Formula(op == '^' ? pr : pr + 1);
    *postfix++ = op;
    *postfix++ = ' ';
  }
}
void Component() {
  int sign;
  if ((sign = *infix) == '+' || *infix == '-') {
    sign = *infix++;
    Formula(30);
    if (sign == '-') {
      *postfix++ = '@';  // unary minus
      *postfix++ = ' ';
    }
  } else if (*infix == '(') {
    infix++;
    Formula(0);
    if (*infix++ != ')')
      error(1);
  } else {
    char* p = infix;
    int sum = 0;
    if (*infix < '0' || *infix > '9')
      error(2);
    while (*infix >= '0' && *infix <= '9') {
      sum = sum * 10 + *infix - '0';
      *postfix++ = *infix++;
    }
    *postfix++ = ' ';
  }
}
int main() {
  cout << "Enter a formula in infix notation: ";
  cin.getline(s, MAXSIZE);
  for (int i = 0; s[i]; i++)  // removes spaces
    if (strchr(" \t", s[i])) {
      s[i] = 0;
      strcat(s, s + i + 1);
    }
  infix = s;
  postfix = r;
  Formula(0);
  *postfix = 0;
  cout << "The equivalent of formula in the postfix form: " << r << endl;
  return 0;
}
