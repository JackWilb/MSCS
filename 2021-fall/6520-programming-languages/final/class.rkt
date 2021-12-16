#lang plait

(define-type Exp
  (castE [to : Symbol]
         [obj : Exp])
  (if0E [if : Exp]
        [thn : Exp]
        [els : Exp])
  (nullE)
  
  (numE [n : Number])
  (plusE [lhs : Exp]
         [rhs : Exp])
  (multE [lhs : Exp]
         [rhs : Exp])
  (argE)
  (thisE)
  (newE [class-name : Symbol]
        [args : (Listof Exp)])
  (getE [obj-expr : Exp]
        [field-name : Symbol])
  (sendE [obj-expr : Exp]
         [method-name : Symbol]
         [arg-expr : Exp])
  (ssendE [obj-expr : Exp]
          [class-name : Symbol]
          [method-name : Symbol]
          [arg-expr : Exp]))

(define-type Class
  (classC [super-name : Symbol]
          [field-names : (Listof Symbol)]
          [methods : (Listof (Symbol * Exp))]))

(define-type Value
  (numV [n : Number])
  (objV [class-name : Symbol]
        [field-values : (Listof Value)])
  (nullV))

(module+ test
  (print-only-errors #t))

;; ----------------------------------------

(define (find [l : (Listof (Symbol * 'a))] [name : Symbol]) : 'a
  (type-case (Listof (Symbol * 'a)) l
    [empty
     (error 'find (string-append "not found: " (symbol->string name)))]
    [(cons p rst-l)
     (if (symbol=? (fst p) name)
         (snd p)
         (find rst-l name))]))

(module+ test
  (test (find (list (values 'a 1)) 'a)
        1)
  (test (find (list (values 'a 1) (values 'b 2)) 'b)
        2)
  (test/exn (find empty 'a)
            "not found: a")
  (test/exn (find (list (values 'a 1)) 'x)
            "not found: x"))

;; ----------------------------------------

(define interp : (Exp (Listof (Symbol * Class)) Value Value -> Value)
  (lambda (a classes this-val arg-val)
    (local [(define (recur expr)
              (interp expr classes this-val arg-val))]
      (type-case Exp a
        [(castE to obj-expr)
         (type-case Value (recur obj-expr)
           [(objV class-name field-vals)
            (if (inherits-from to class-name (reverse classes))
                (objV class-name field-vals)
                (error 'interp "cannot cast to that"))]
           [else (error 'interp "not an object")])]
        [(if0E i t e)
         (let ([interped-i (recur i)])
           (type-case Value interped-i
             [(numV n)
              (if (equal? 0 n)
                  (recur t)
                  (recur e))]
             [else (error 'interp "not a number")]))]
        [(nullE) (nullV)]
        
        [(numE n) (numV n)]
        [(plusE l r) (num+ (recur l) (recur r))]
        [(multE l r) (num* (recur l) (recur r))]
        [(thisE) this-val]
        [(argE) arg-val]
        [(newE class-name field-exprs)
         (local [(define c (find classes class-name))
                 (define vals (map recur field-exprs))]
           (if (= (length vals) (length (classC-field-names c)))
               (objV class-name vals)
               (error 'interp "wrong field count")))]
        [(getE obj-expr field-name)
         (type-case Value (recur obj-expr)
           [(objV class-name field-vals)
            (type-case Class (find classes class-name)
              [(classC super-name field-names methods)
               (find (map2 (lambda (n v) (values n v))
                           field-names
                           field-vals)
                     field-name)])]
           [(nullV) (error 'interp "get on null")]
           [else (error 'interp "not an object")])]
        [(sendE obj-expr method-name arg-expr)
         (local [(define obj (recur obj-expr))
                 (define arg-val (recur arg-expr))]
           (type-case Value obj
             [(objV class-name field-vals)
              (call-method class-name method-name classes
                           obj arg-val)]
             [(nullV) (error 'interp "send on null")]
             [else (error 'interp "not an object")]))]
        [(ssendE obj-expr class-name method-name arg-expr)
         (local [(define obj (recur obj-expr))
                 (define arg-val (recur arg-expr))]
           (call-method class-name method-name classes
                        obj arg-val))]))))

(define (call-method class-name method-name classes
                     obj arg-val)
  (type-case Class (find classes class-name)
    [(classC super-name field-names methods)
     (let ([body-expr (find methods method-name)])
       (interp body-expr
               classes
               obj
               arg-val))]))

(define (num-op [op : (Number Number -> Number)]
                [op-name : Symbol] 
                [x : Value]
                [y : Value]) : Value
  (cond
    [(and (numV? x) (numV? y))
     (numV (op (numV-n x) (numV-n y)))]
    [else (error 'interp "not a number")]))

(define (num+ x y) (num-op + '+ x y))
(define (num* x y) (num-op * '* x y))

;; ----------------------------------------
;; Examples

(module+ test
  (define posn-class
    (values 'Posn
            (classC 'Object
             (list 'x 'y)
             (list (values 'mdist
                           (plusE (getE (thisE) 'x) (getE (thisE) 'y)))
                   (values 'addDist
                           (plusE (sendE (thisE) 'mdist (numE 0))
                                  (sendE (argE) 'mdist (numE 0))))
                   (values 'addX
                           (plusE (getE (thisE) 'x) (argE)))
                   (values 'multY (multE (argE) (getE (thisE) 'y)))
                   (values 'factory12 (newE 'Posn (list (numE 1) (numE 2))))))))
    
  (define posn3D-class
    (values 'Posn3D
            (classC 'Posn
             (list 'x 'y 'z)
             (list (values 'mdist (plusE (getE (thisE) 'z)
                                         (ssendE (thisE) 'Posn 'mdist (argE))))
                   (values 'addDist (ssendE (thisE) 'Posn 'addDist (argE)))))))

  (define posn27 (newE 'Posn (list (numE 2) (numE 7))))
  (define posn531 (newE 'Posn3D (list (numE 5) (numE 3) (numE 1))))

  (define (interp-posn a)
    (interp a (list posn-class posn3D-class) (numV -1) (numV -1))))

;; ----------------------------------------

(module+ test
  (test (interp-posn (castE 'Object posn27))
        (objV 'Posn (list (numV 2) (numV 7))))
  (test (interp-posn (castE 'Posn posn27))
        (objV 'Posn (list (numV 2) (numV 7))))
  (test/exn (interp-posn (castE 'Posn3D posn27))
            "cannot cast to that")
  (test/exn (interp-posn (castE 'Object (numE 2)))
            "not an object")
  
  (test (interp-posn (if0E (numE 0)
                           (numE 2)
                           (numE 3)))
        (numV 2))
  (test (interp-posn (if0E (numE 1)
                           (numE 2)
                           (numE 3)))
        (numV 3))
  (test (interp-posn (if0E (sendE posn27 'addX (numE -2))
                           (numE 2)
                           (numE 3)))
        (numV 2))
  (test/exn (interp-posn (if0E (newE 'Posn (list (numE 2) (numE 7)))
                           (numE 2)
                           (numE 3)))
        "not a number")
  (test (interp-posn (nullE))
        (nullV))
  (test (interp-posn (sendE (ssendE (nullE) 'Posn 'factory12 (numE 0))
                            'multY
                            (numE 15)))
        (numV 30))
  (test/exn (interp-posn (sendE (ssendE (nullE) 'Posn 'multY (numE 0))
                                'multY
                                (numE 15)))
            "get on null")
  (test/exn (interp-posn (getE (nullE) 'x))
            "get on null")
  (test/exn (interp-posn (sendE (nullE) 'mdist (numE 0)))
            "send on null")
  (test/exn (interp-posn (ssendE (nullE) 'Posn 'mdist (numE 0)))
            "get on null")
  (test/exn (interp-posn (plusE (numE 1) (nullE)))
            "not a number")

  
  (test (interp (numE 10) 
                empty (objV 'Object empty) (numV 0))
        (numV 10))
  (test (interp (plusE (numE 10) (numE 17))
                empty (objV 'Object empty) (numV 0))
        (numV 27))
  (test (interp (multE (numE 10) (numE 7))
                empty (objV 'Object empty) (numV 0))
        (numV 70))

  (test (interp-posn (newE 'Posn (list (numE 2) (numE 7))))
        (objV 'Posn (list (numV 2) (numV 7))))

  (test (interp-posn (sendE posn27 'mdist (numE 0)))
        (numV 9))
  
  (test (interp-posn (sendE posn27 'addX (numE 10)))
        (numV 12))

  (test (interp-posn (sendE (ssendE posn27 'Posn 'factory12 (numE 0))
                            'multY
                            (numE 15)))
        (numV 30))

  (test (interp-posn (sendE posn531 'addDist posn27))
        (numV 18))
  
  (test/exn (interp-posn (plusE (numE 1) posn27))
            "not a number")
  (test/exn (interp-posn (getE (numE 1) 'x))
            "not an object")
  (test/exn (interp-posn (sendE (numE 1) 'mdist (numE 0)))
            "not an object")
  (test/exn (interp-posn (ssendE (numE 1) 'Posn 'mdist (numE 0)))
            "not an object")
  (test/exn (interp-posn (newE 'Posn (list (numE 0))))
            "wrong field count"))


















;; new helpers

(define (inherits-from [name : Symbol] [obj-class-name : Symbol] [classes : (Listof (Symbol * Class))]) : Boolean
  (type-case (Listof (Symbol * Class)) classes
    [empty #f]
    [(cons f r) (if (equal? obj-class-name (fst f))
                    (type-case Class (snd f)
                      [(classC super-name fields methods)
                       (if (or (equal? name obj-class-name) (equal? name super-name))
                           #t
                           (inherits-from name super-name r))])
                    (inherits-from name obj-class-name r))]))

(module+ test
  (test (inherits-from 'a 'a (list))
        #f))
