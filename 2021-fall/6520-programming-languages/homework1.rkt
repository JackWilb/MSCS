#lang plait

(print-only-errors #t)

(define-type Tree
  (leaf [val : Number])
  (node [val : Number]
        [left : Tree]
        [right : Tree]))

#; Part1
(define (sum [t : Tree]) : Number
  (type-case Tree t
    [(leaf v) v]
    [(node v l r) (+ v (+ (sum l) (sum r)))]))

(test (sum (leaf 7))
      7)
(test (sum (leaf -7))
      -7)
(test (sum (node 5 (leaf 6) (leaf 7)))
      18)
(test (sum (node 0 (leaf 0) (leaf 0)))
      0)


#; Part2
(define (negate [t : Tree]) : Tree
  (type-case Tree t
    [(leaf v) (leaf (- 0 v))]
    [(node v l r) (node (- 0 v) (negate l) (negate r))]))

(test (negate (leaf 7))
      (leaf -7))
(test (negate (leaf -7))
      (leaf 7))
(test (negate (node 5 (leaf 6) (leaf 7)))
      (node -5 (leaf -6) (leaf -7)))
(test (negate (node 0 (leaf 0) (leaf 0)))
      (node 0 (leaf 0) (leaf 0)))


#; Part3
(define (contains? [t : Tree] [n : Number]) : Boolean
  (type-case Tree t
    [(leaf v) (equal? v n)]
    [(node v l r) (or (equal? v n) (or (contains? l n) (contains? r n)))]))

(test (contains? (leaf 7) 7)
      #t)
(test (contains? (node 5 (leaf 6) (leaf 7)) 6)
      #t)
(test (contains? (node 5 (leaf 6) (leaf 7)) 7)
      #t)
(test (contains? (node 5 (leaf 6) (leaf 7)) 5)
      #t)
(test (contains? (node 5 (leaf 6) (leaf 7)) 0)
      #f)
(test (contains? (node 0 (leaf 0) (leaf 0)) 0)
      #t)


#; Part4
(define (bigger-leaves? [t : Tree] [n : Number]) : Boolean
  (type-case Tree t
    [(leaf v) (> v n)]
    [(node v l r) (and (bigger-leaves? l (+ n v)) (bigger-leaves? r (+ n v)))]))

(define (big-leaves? [t : Tree]) : Boolean
  (type-case Tree t
    [(leaf v) #t]
    [(node v l r) (and (bigger-leaves? l v) (bigger-leaves? r v))]))

(test (big-leaves? (node 5 (leaf 6) (leaf 7)))
      #t)
(test (big-leaves? (node 5 (node 2 (leaf 8) (leaf 6)) (leaf 7)))
      #f)
(test (big-leaves? (leaf 7))
      #t)


#; Part5
(define (positive-trees? [lt : (Listof Tree)]) : Boolean
  (type-case (Listof Tree) lt
    [empty #t]
    [(cons t rest) (and (> (sum t) 0) (positive-trees? rest))]))

(test (positive-trees? empty)
      #t)
(test (positive-trees? (cons (leaf 6)
                             empty))
      #t)
(test (positive-trees? (cons (leaf -6)
                             empty))
      #f)
(test (positive-trees? (cons (node 1 (leaf 6) (leaf -6))
                             empty))
      #t)
(test (positive-trees? (cons (node 1 (leaf 6) (leaf -6))
                             (cons (node 0 (leaf 0) (leaf 1))
                                   empty)))
      #t)
(test (positive-trees? (cons (node -1 (leaf 6) (leaf -6))
                             (cons (node 0 (leaf 0) (leaf 1))
                                   empty)))
      #f)
