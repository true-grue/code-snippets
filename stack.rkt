#lang racket

(require redex)

(define-language stack-lang
  (op ::= + - * / dup drop swap)
  (val ::= number)
  (cmd ::= op val)
  (prog ::= (void ... cmd ...))
  (st ::= (val ...))
  (E ::= hole (void ... E cmd ...)))

(define stack-red
  (reduction-relation stack-lang
   #:domain (prog st)
   (--> [(in-hole E val_1) (val ...)]
        [(in-hole E void) (val_1 val ...)]
        "literal")
   (--> [(in-hole E dup) (val_1 val ...)]
        [(in-hole E void) (val_1 val_1 val ...)]
        "dup")
   (--> [(in-hole E drop) (val_1 val ...)]
        [(in-hole E void) (val ...)]
        "drop")
   (--> [(in-hole E swap) (val_1 val_2 val ...)]
        [(in-hole E void) (val_2 val_1 val ...)]
        "swap")
   (--> [(in-hole E +) (val_1 val_2 val ...)]
        [(in-hole E void) (val_3 val ...)]
        (where val_3 ,(+ (term val_2) (term val_1)))
        "+")
   (--> [(in-hole E -) (val_1 val_2 val ...)]
        [(in-hole E void) (val_3 val ...)]
        (where val_3 ,(- (term val_2) (term val_1)))
        "-")
   (--> [(in-hole E *) (val_1 val_2 val ...)]
        [(in-hole E void) (val_3 val ...)]
        (where val_3 ,(* (term val_2) (term val_1)))
        "*")
   (--> [(in-hole E /) (val_1 val_2 val ...)]
        [(in-hole E void) (val_3 val ...)]
        (where val_3 ,(/ (term val_2) (term val_1)))
        "/")
   (--> [(void void ...) st]
        [() st]
        "cleanup")
   ))

(test-->> stack-red (term ((dup * 1 -) (4))) (term (() (15))))
  