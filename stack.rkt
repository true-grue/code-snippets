#lang racket

(require redex)

(define-language stack-lang
  (op ::= + - * / dup drop swap)
  (lit ::= number)
  (cmd ::= op lit)
  (prog ::= [(cmd ...) (lit ...)]))

(define stack-red
  (reduction-relation stack-lang
   #:domain prog
   (--> [(lit_1 cmd ...) (lit ...)]
        [(cmd ...) (lit_1 lit ...)]
        "literal")
   (--> [(dup cmd ...) (lit_1 lit ...)]
        [(cmd ...) (lit_1 lit_1 lit ...)]
        "dup")
   (--> [(drop cmd ...) (lit_1 lit ...)]
        [(cmd ...) (lit ...)]
        "drop")
   (--> [(swap cmd ...) (lit_1 lit_2 lit ...)]
        [(cmd ...) (lit_2 lit_1 lit ...)]
        "swap")
   (--> [(+ cmd ...) (lit_1 lit_2 lit ...)]
        [(cmd ...) (lit_3 lit ...)]
        (where lit_3 ,(+ (term lit_2) (term lit_1)))
        "+")
   (--> [(- cmd ...) (lit_1 lit_2 lit ...)]
        [(cmd ...) (lit_3 lit ...)]
        (where lit_3 ,(- (term lit_2) (term lit_1)))
        "-")
   (--> [(* cmd ...) (lit_1 lit_2 lit ...)]
        [(cmd ...) (lit_3 lit ...)]
        (where lit_3 ,(* (term lit_2) (term lit_1)))
        "*")
   (--> [(/ cmd ...) (lit_1 lit_2 lit ...)]
        [(cmd ...) (lit_3 lit ...)]
        (where lit_3 ,(/ (term lit_2) (term lit_1)))
        "/")))

(test-->> stack-red (term [(dup * 1 -) (4)]) (term [() (15)]))
  