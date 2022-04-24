## Task 3.1** Implement parser combinators in a programming language of your choice which supports higher-order functions. At least the following combinators must be implemented:

	- string or regex parser
	- sequence (a, b )
	- Kleene star
	- composition (a · b: parse a, pass result to b; if b fails, whole composition fails)
	- lookahead (a | b : parse a, try parse b, if b succeeds, continue parsing from the last part of a)
	
	Implementation on Python
	