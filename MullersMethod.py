"""
Implementation of Muller's method
Approximates one of the roots for an equation of the form f(x) = 0

Contributors:
Archana 
Arun 
"""

from cmath import *
from itertools import count as counting_forever
TOLERATED_PERCENTAGE_ERROR = 10 ** (-3)
MAX_ITERATIONS = 100
DEBUG = False

def find_next_guess(func, x0, x1, x2):
    # print(x0, x1, x2)
    e = func(x0)
    f = func(x1)
    g = func(x2)

    # test4.1 and test5 throw ZeroDivisionErrors here.
    # While we can except and check if f(0) = 0, is that the only kind of case 
    # that will throw such an error?
    h0 = x1 - x0
    h1 = x2 - x1
    delta0 = (f - e) / h0
    delta1 = (g - f) / h1

    a = (delta1 - delta0) / (h1 + h0) 
    b = (a * h1) + delta1
    c = g
    d = sqrt((b * b) - (4 * a * c)) # Square root of discriminant
    
    if abs(b - d) > abs(b + d): # The denominator should have a large magnitude.
        x3 = x2 - ((2 * c) / (b - d))
    else:
        x3 = x2 - ((2 * c) / (b + d))

    return x3

def read_inputs(disable_prompts = False):

    prompt = "Enter the function: " if not disable_prompts else ""            
    expr = input(prompt)
    expr = expr.replace("^", "**") #** is used for pow in Python
    expr = expr.replace("i", "j")
    func = lambda x: eval(expr) # Assuming "x" is the independent var
    # Caution: Python uses j for sqrt(-1)

    #TODO Support for natural mathematic notation
    #TODO Input validation

    def read_guess(guess_no):
        prompt = f"Initial guess {guess_no}: " if not disable_prompts else ""
        x = input(prompt)
        x = x.replace("i", "j")
        x = complex(x)
        return x

    x0, x1, x2 = read_guess(0), read_guess(1), read_guess(2)

    if isclose(x0, x1) or isclose(x1, x2) or isclose(x2, x0):
        raise ValueError("At least two of the three guesses are the same.")


    return func, x0, x1, x2

def main():
    
    func, x0, x1, x2 = read_inputs(disable_prompts = DEBUG)

    for iteration_cnt in counting_forever(1): 

        x3 = find_next_guess(func, x0, x1, x2)

        # is all is required? Plus TODO ZeroDivisionError for x3

        if isclose(x2, x3, rel_tol = TOLERATED_PERCENTAGE_ERROR, abs_tol = TOLERATED_PERCENTAGE_ERROR)\
           or iteration_cnt >= MAX_ITERATIONS:
            print("One of the roots is: ", f"{x3 : .4f}".replace("j", "i")) # Is the precision bad?
            print(f"No. of iterations = {iteration_cnt}")
            print(f"Verification: f({str(x3).replace('j', 'i')}) = {str(func(x3)).replace('j', 'i')}")
            break
            
        else:
            x0, x1, x2 = x1, x2, x3

if __name__ == "__main__": main()

"""
TEST CASES

#1
stdin:
x^3 - 13*x - 12
4.5
5.5
5.0

stdout:
4.0

#2
stdin:
x^4 - 3*x^2 + x - 10
2
2.5
3

stdout:
2.1624

We need test cases for non-polynomial functions too.
"""      
