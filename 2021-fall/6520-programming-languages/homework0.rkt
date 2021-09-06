#lang plait

#; Part1
(define (3rd-power x)
  (* x (* x x)))

(test (3rd-power 1)
       1)
(test (3rd-power 2)
       8)
(test (3rd-power 17)
       4913)


#; Part2
(define (6th-power x)
  (* (3rd-power x) (3rd-power x)))

(define (12th-power x)
  (* (6th-power x) (6th-power x)))

(define (24th-power x)
  (* (12th-power x) (12th-power x)))

(define (42nd-power x)
  (* (* (24th-power x) (12th-power x)) (6th-power x)))

(test (42nd-power 1)
       1)
(test (42nd-power 2)
       4398046511104)
(test (42nd-power 17)
       4773695331839566234818968439734627784374274207965089)


#; Part3
(define (plural str)
  (if (equal? (string-length str) 0)
      "s"
      (if (equal? (string-ref str (- (string-length str) 1)) #\y)
          (string-append (substring str 0 (- (string-length str) 1)) "ies")
          (string-append str "s"))))

(test (plural "")
      "")
(test (plural "baby")
      "babies")
(test (plural "fruit")
      "fruits")
(test (plural "fruity")
      "fruities")


#; Part4
(define-type Light
  (bulb [watts : Number]
        [technology : Symbol])
  (candle [inches : Number]))

(define (energy-usage [l : Light]): Number
  (type-case Light l
    [(bulb w t) (/ (* 24 w) 1000)]
    [(candle i) 0]))

(test (energy-usage (bulb 100.0 'halogen))
      2.4)
(test (energy-usage (bulb 5.0 'LED))
      0.12)
(test  (energy-usage (candle 10.0))
      0)


#; Part5
(define (use-for-one-hour [l : Light]) : Light
  (type-case Light l
    [(bulb w t) (bulb w t)]
    [(candle i) (if (>= i 1)
                    (candle (- i 1))
                    (candle 0.0))]))

(test (use-for-one-hour (bulb 100.0 'halogen))
      (bulb 100.0 'halogen))
(test (use-for-one-hour (candle 10.0))
      (candle 9.0))
(test (use-for-one-hour (candle 1.0))
      (candle 0.0))
(test (use-for-one-hour (candle 0.5))
      (candle 0.0))
(test (use-for-one-hour (candle 0.0))
      (candle 0.0))
