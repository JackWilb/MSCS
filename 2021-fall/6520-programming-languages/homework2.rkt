#lang plait

(define-type Exp
  (numE [n : Number])
  (idE [s : Symbol])
  (plusE [l : Exp] 
         [r : Exp])
  (multE [l : Exp]
         [r : Exp])
  ;; Added maxE
  (maxE [l : Exp]
         [r : Exp])
  ;; Modified arg to Listof Exp
  (appE [s : Symbol]
        [arg : (Listof Exp)]))

;; Modified arg to Listof Symbol
(define-type Func-Defn
  (fd [name : Symbol] 
      [arg : (Listof Symbol)] 
      [body : Exp]))

(module+ test
  (print-only-errors #t))

;; An EXP is either
;; - `NUMBER
;; - `SYMBOL
;; - `{+ EXP EXP}
;; - `{* EXP EXP}
;; - `{SYMBOL EXP)

;; A FUNC-DEFN is
;; - `{define {SYMBOL SYMBOL} EXP}

;; parse ----------------------------------------
(define (parse [s : S-Exp]) : Exp
  (cond
    [(s-exp-match? `NUMBER s) (numE (s-exp->number s))]
    [(s-exp-match? `SYMBOL s) (idE (s-exp->symbol s))]
    [(s-exp-match? `{+ ANY ANY} s)
     (plusE (parse (second (s-exp->list s)))
            (parse (third (s-exp->list s))))]
    [(s-exp-match? `{* ANY ANY} s)
     (multE (parse (second (s-exp->list s)))
            (parse (third (s-exp->list s))))]
    ;; Added maxE
    [(s-exp-match? `{max ANY ANY} s)
     (maxE (parse (second (s-exp->list s)))
            (parse (third (s-exp->list s))))]

    ;; Added ... for functions with 1 or more args
    [(s-exp-match? `{SYMBOL ANY ...} s)
     (appE (s-exp->symbol (first (s-exp->list s)))
           (map parse (rest (s-exp->list s))))]
    [else (error 'parse "invalid input")]))

(define (parse-fundef [s : S-Exp]) : Func-Defn
  (cond
  
    ;; Added match for 1 or more function arguments
    [(s-exp-match? `{define {SYMBOL ANY ...} ANY} s)
     (fd (s-exp->symbol (first (s-exp->list (second (s-exp->list s)))))
         (check-var-names (map s-exp->symbol (rest (s-exp->list (second (s-exp->list s))))))
         (parse (third (s-exp->list s))))]
    [else (error 'parse-fundef "invalid input")]))

(define (check-var-names [syms : (Listof Symbol)]) : (Listof Symbol)
  (type-case (Listof Symbol) syms
    [empty empty]
    [(cons s rst) (if (check-var-names-helper syms)
                   (error 'check-var-names "bad syntax: repeated symbol")
                   syms)]))

(define (check-var-names-helper [syms : (Listof Symbol)]) : Boolean
  (type-case (Listof Symbol) syms
    [empty #f]
    [(cons s rst) (or (member s rst) (check-var-names-helper rst))]))

(module+ test
  (test (parse `2)
        (numE 2))
  (test (parse `x)
        (idE 'x))
  (test (parse `{+ 2 1})
        (plusE (numE 2) (numE 1)))
  (test (parse `{* 3 4})
        (multE (numE 3) (numE 4)))
  (test (parse `{+ {* 3 4} 8})
        (plusE (multE (numE 3) (numE 4))
               (numE 8)))

  ;; Added max test
  (test (parse `{max 2 1})
        (maxE (numE 2) (numE 1)))
  (test (parse `{+ {max 2 1} {max -1 0}})
        (plusE (maxE (numE 2) (numE 1)) (maxE (numE -1) (numE 0))))
  
  (test (parse `{double 9})
        (appE 'double (list (numE 9))))
  (test/exn (parse `{{+ 1 2}})
            "invalid input")

  (test (parse-fundef `{define {double x} {+ x x}})
        (fd 'double (list 'x) (plusE (idE 'x) (idE 'x))))
  
  
  (test/exn (parse-fundef `{def {f x} x})
            "invalid input")

  (define double-def
    (parse-fundef `{define {double x} {+ x x}}))
  (define quadruple-def
    (parse-fundef `{define {quadruple x} {double {double x}}}))

  ;; Added parse and fundef-parse tests
    (test (parse `{five})
        (appE 'five empty))
    (test (parse `{add 9 10})
        (appE 'add (list (numE 9) (numE 10))))
  (test (parse-fundef `{define {five} 5})
        (fd 'five empty (numE 5)))
  (test (parse-fundef `{define {add x y} {+ x y}})
        (fd 'add (list 'x 'y) (plusE (idE 'x) (idE 'y))))

  ;; check-var-names tests
  (test (check-var-names empty)
        empty)
  (test (check-var-names (list 'x))
        (list 'x))
  (test/exn (check-var-names (list 'x 'x))
        "bad syntax")
  (test/exn (parse-fundef `{define {f x x} x})
        "bad syntax")
  )

;; interp ----------------------------------------
(define (interp [a : Exp] [defs : (Listof Func-Defn)]) : Number
  (type-case Exp a
    [(numE n) n]
    [(idE s) (error 'interp "free variable")]
    [(plusE l r) (+ (interp l defs) (interp r defs))]
    [(multE l r) (* (interp l defs) (interp r defs))]
    ;; Added maxE
    [(maxE l r) (max (interp l defs) (interp r defs))]
    
    [(appE s args) (local [(define fd (get-fundef s defs))]
                    (interp (subst-list (interp-list args defs)
                                   (fd-arg fd)
                                   (fd-body fd))
                            defs))]))

(define (interp-list [expns : (Listof Exp)] [defs : (Listof Func-Defn)]) : (Listof Exp)
  (type-case (Listof Exp) expns
      [empty empty]
      [(cons e rst) (cons (numE (interp e defs)) (interp-list rst defs))]))
  

(module+ test
  (test (interp (parse `2) empty)
        2)
  (test/exn (interp (parse `x) empty)
            "free variable")
  (test (interp (parse `{+ 2 1}) empty)
        3)
  (test (interp (parse `{* 2 1}) empty)
        2)
  (test (interp (parse `{+ {* 2 3}
                           {+ 5 8}})
                empty)
        19)

  ;; Added max interp test
  (test (interp (parse `{max 2 1}) empty)
        2)
  (test (interp (parse `{+ {max 2 1} {max -1 0}}) empty)
        2)
  
  (test (interp (parse `{double 8})
                (list double-def))
        16)
  (test (interp (parse `{quadruple 8})
                (list double-def quadruple-def))
        32)

  ;; Added new interp tests
  (test (interp-list (list (parse `2)) empty)
        (list (numE 2)))
  (test (interp-list (list (parse `2) (parse `4) (parse `5)) empty)
        (list (numE 2) (numE 4) (numE 5)))
  (test (interp (parse `{f 1 2})
                (list (parse-fundef `{define {f x y} {+ x y}})))
        3)
  (test (interp (parse `{+ {f} {f}})
                (list (parse-fundef `{define {f} 5})))
        10)
  (test (interp (parse `{f 2 3})
                (list (parse-fundef `{define {f x y} {+ y {+ x x}}})))
        7)
  (test/exn (interp (parse `{f 1})
                    (list (parse-fundef `{define {f x y} {+ x y}})))
            "wrong arity"))


;; get-fundef ----------------------------------------
(define (get-fundef [s : Symbol] [defs : (Listof Func-Defn)]) : Func-Defn
  (type-case (Listof Func-Defn) defs
    [empty (error 'get-fundef "undefined function")]
    [(cons def rst-defs) (if (eq? s (fd-name def))
                             def
                             (get-fundef s rst-defs))]))

(module+ test
  (test (get-fundef 'double (list double-def))
        double-def)
  (test (get-fundef 'double (list double-def quadruple-def))
        double-def)
  (test (get-fundef 'double (list quadruple-def double-def))
        double-def)
  (test (get-fundef 'quadruple (list quadruple-def double-def))
        quadruple-def)
  (test/exn (get-fundef 'double empty)
            "undefined function"))

;; subst ----------------------------------------
(define (subst [what : Exp] [for : Symbol] [in : Exp])
  (type-case Exp in
    [(numE n) in]
    [(idE s) (if (eq? for s)
                 what
                 in)]
    [(plusE l r) (plusE (subst what for l)
                        (subst what for r))]
    [(multE l r) (multE (subst what for l)
                        (subst what for r))]
    ;; Added maxE
    [(maxE l r) (maxE (subst what for l)
                      (subst what for r))]
    
    [(appE s args) (appE s (subst-args what for args))]))

(define (subst-list [what : (Listof Exp)] [for : (Listof Symbol)] [in : Exp]) : Exp
  (type-case (Listof Exp) what
    [empty in]
    [(cons e rst) (if (equal? (length what) (length for))
                   (subst-list (rest what) (rest for) (subst (first what) (first for) in))
                   (error 'subst-list "wrong arity"))]))

(define (subst-args [what : Exp] [for : Symbol] [in : (Listof Exp)]) : (Listof Exp)
  (type-case (Listof Exp) in
    [empty empty]
    [(cons e rst) (cons (subst what for e) (subst-args what for rst))]))

(module+ test
  (test (subst (parse `8) 'x (parse `9))
        (numE 9))
  (test (subst (parse `8) 'x (parse `x))
        (numE 8))
  (test (subst (parse `8) 'x (parse `y))
        (idE 'y))
  (test (subst (parse `8) 'x (parse `{+ x y}))
        (parse `{+ 8 y}))
  (test (subst (parse `8) 'x (parse `{* y x}))
        (parse `{* y 8}))

  ;; Added max subst tests
    (test (subst (parse `8) 'x (parse `{max y x}))
        (parse `{max y 8}))
  
  (test (subst (parse `8) 'x (parse `{double x}))
        (parse `{double 8}))

  ;; Add 2 subst with multiple args
  (test (subst (parse `10) 'x (parse `{add x y}))
        (parse `{add 10 y}))
  (test (subst (parse `9) 'y (parse `{add x y}))
        (parse `{add x 9}))

  ;; Added test for subst-list
   (test (subst-list (list (parse `8)) (list 'x) (parse `x))
        (numE 8))
  (test (subst-list (list (parse `8) (parse `9)) (list 'x 'y) (parse `{+ x y}))
        (plusE (numE 8) (numE 9)))
  (test (subst-list (list (parse `8) (parse `9)) (list 'y 'x) (parse `{+ x y}))
        (plusE (numE 9) (numE 8)))
  )
