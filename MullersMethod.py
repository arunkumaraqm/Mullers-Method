"""
Implementation of Muller's method
Approximates one of the roots for an equation of the form f(x) = 0

Contributors:
Archana (ENG18CS0044)
Arun (ENG18CS0047)
"""

from cmath import * # It provides access to mathematical functions for complex numbers like complex().
from itertools import count as counting_forever # This module provides access to iterators like count().
TOLERATED_PERCENTAGE_ERROR = 10 ** (-3) # accepted percentage error upto 0.001
MAX_ITERATIONS = 100 
DEBUG = True

def find_next_guess(func, x0, x1, x2): # Defining a function find_next_guess()
    #print(x0, x1, x2)
    try: # The try block lets you test a block of code for errors.
        e = func(x0) # calculating the function value at x0
        f = func(x1) # calculating the function value at x1
        g = func(x2) # calculating the function value at x2
    except: #The except block lets you handle the error.
        raise ValueError("The function does not meet input criteria.")
        
    try:
        h0 = x1 - x0
        h1 = x2 - x1
        delta0 = (f - e) / h0
        delta1 = (g - f) / h1

        a = (delta1 - delta0) / (h1 + h0) 
        b = (a * h1) + delta1
        c = g
        d = sqrt((b * b) - (4 * a * c)) # Square root of discriminant
        
        #print(h0, h1, delta0, delta1, a, b, c, d)
        
        if abs(b - d) > abs(b + d): # The denominator should have a large magnitude.
            x3 = x2 - ((2 * c) / (b - d))
        else:
            x3 = x2 - ((2 * c) / (b + d))

    except ZeroDivisionError as err: #The except block lets you handle the error.
        if isclose(func(0), 0):
            x3 = 0
        else:
            raise ZeroDivisionError(str(err) + "; we haven't thought this through.")
    finally: #The finally block will be executed regardless if the try block raises an error or not.
        return x3

def read_inputs(disable_prompts = False): # Defining a function read_inputs() 

    prompt = "Enter the function: " if not disable_prompts else ""            
    expr = input(prompt)
    expr = expr.replace("^", "**") #** is used for pow in Python
    func = lambda x: eval(expr) # Assuming "x" is the independent var
    # Caution: Python uses j for sqrt(-1)

    #TODO Support for natural mathematic notation
    #TODO Input validation

    def read_guess(guess_no): # Defining a function read_guess
        prompt = f"Initial guess {guess_no}: " if not disable_prompts else ""
        x = input(prompt)
        x = complex(x) """ The complex() method returns a complex number when real and imaginary parts are provided,
                           or it converts a string to a complex number."""
        return x

    x0, x1, x2 = read_guess(0), read_guess(1), read_guess(2) # copying the values of the functions to x0,x1,x2

    if isclose(x0, x1) or isclose(x1, x2) or isclose(x2, x0): """ method checks whether two values are close, or not. 
                                                   This method returns a Boolean value: True if the values are close, otherwise False."""
        raise ValueError("At least two of the three guesses are the same.")


    return func, x0, x1, x2

def main(): # Defining a function main()
    
    func, x0, x1, x2 = read_inputs(disable_prompts = DEBUG)

    for iteration_cnt in counting_forever(1): # counting_forever  starts counting from 1

        x3 = find_next_guess(func, x0, x1, x2)

        # is all is required? Plus TODO ZeroDivisionError for x3

        if isclose(x2, x3, rel_tol = TOLERATED_PERCENTAGE_ERROR, abs_tol = TOLERATED_PERCENTAGE_ERROR)\
           or iteration_cnt >= MAX_ITERATIONS: """ rel_tol is the relative tolerance. It is the maximum allowed difference
                                                   between value x2 and x3. 
                                                   In this case rel_tol=0.001 . abs_tol is the minimum absolute tolerance. 
                                                   It is used to compare values near 0. 
                                                   The value must be at least 0. In this case abs_tol=0.001 """
            print(f"One of the roots is: {x3 : .4f}") # Is the precision bad?
            print(f"No. of iterations = {iteration_cnt}")
            print(f"Verification: f({x3}) = {func(x3)}")
            break
            
        else:
            x0, x1, x2 = x1, x2, x3

if __name__ == "__main__": main() """ if __name__ == "__main__" is used to execute some code only if the file was run directly, 
                                      and not imported."""

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
