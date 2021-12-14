# Final Assignment

Below I detail which of the additions I made to the language and what descisions I made to implement them.

### Casting

I added casting by using some logic from homework #9 to add inherritance hints to the class.rkt file (that deals with Exps, not ExpIs). The inherritance hints allow that layer to determine if the Exp to cast is the same type or a subtype of the symbol passed in. The logic is almost identical to homework #9, where we were checking for instanceof.

For the type system, I set it up as requested. The type checker doesn't complain if the expression is a sub or super type of the symbol. This means the type system allows things that could break, but the interpreter will catch them.

### if0

I added an if0 form to all layers of the language (except typed-parse). The implementation of interp was pretty standard, even with the inherritance layers. The main trickiness came when I implemented the type checking in my least upper bound function, lub. I fixed one class and then tested each super type of the other class until there was a match or we ran out of classes to check. If there was a match (is-subtype was true), I returned the parent that was the least upper bound. This works because one of the parent classes must be a parent type for both object. Since lub was the hard part, most of my testing is in typed-class.


## Total stars earned
- (#1 1 star) Casting
- (#2 2 star) if0
