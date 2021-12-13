# Final Assignment

Below I detail which of the additions I made to the language and what descisions I made to implement them.

### Casting

I added casting
Total 1 star by using some logic from homework #9 to add inherritance hints to the class.rkt file (that deals with Exps, not ExpIs). The inherritance hints allow that layer to determine if the Exp to cast is the same type or a subtype of the symbol passed in. The logic is almost identical to homework #9, where we were checking for instanceof.

For the type system, I set it up as requested. The type checker doesn't complain if the expression is a sub or super type of the symbol. This means the type system allows things that could break, but the interpreter will catch them.

## Total stars earned
- (1 star) Casting
