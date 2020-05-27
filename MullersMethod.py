"""
Implementation of Muller's method
Approximates one of the roots for an equation of the form f(x) = 0
This implementation supports complex functions and complex guesses.

Contributors:
Archana (ENG18CS0044)
Arun (ENG18CS0047)
"""

from cmath import * # It provides access to mathematical functions for complex numbers like sinh() nad abs().
from itertools import count as counting_forever # This module provides access to iterators like count().

# Defining constraints
TOLERATED_PERCENTAGE_ERROR = 10 ** (-3) # accepted percentage error upto 0.001
MAX_ITERATIONS = 100 

DEBUG = False

def find_next_guess(func, x0, x1, x2): 

    try: # The try block lets you test a block of code for errors.
    # calculating the function values at x0, x1 and x2
        e = func(x0) 
        f = func(x1) 
        g = func(x2) 
    except: #The except block lets you handle the error.
        raise ValueError("The function does not meet input criteria.")
        # This could be because the entered function does not conform to Python syntax.
        # or because the function is not analytic at a point x.
        
    try:
        h0 = x1 - x0
        h1 = x2 - x1
        delta0 = (f - e) / h0
        delta1 = (g - f) / h1

        a = (delta1 - delta0) / (h1 + h0) 
        b = (a * h1) + delta1
        c = g
        d = sqrt((b * b) - (4 * a * c)) # discriminant
        
        # The denominator should have a large magnitude so that x3 is closer to x2.
        if abs(b - d) > abs(b + d): 
            x3 = x2 - ((2 * c) / (b - d))
        else:
            x3 = x2 - ((2 * c) / (b + d))

    except ZeroDivisionError as err: 
        """
        During testing, we discovered that if the root of the function is 0,
        x2 eventually reaches the value 0, then g = f(x2) = 0.
        This ends up making h1 + h0 = 0 or b - d = 0 or b + d = 0 depending on the other values.
        So, we require this except block.
        """
        
        if isclose(func(0), 0): # Checking if 0 is a root.
            x3 = 0
        else:
            # As per our calculations, control will never reach this block.
            raise ZeroDivisionError(str(err) + "; we haven't thought this through.")
    
    finally: # The finally block will be executed regardless if the try block raises an error or not.
        return x3

def read_inputs(disable_prompts = False): 

    prompt = "Enter the function: " if not disable_prompts else ""            
    expr = input(prompt) # should not end with ' = 0' obviously.

    # Converting the input string to a Python expression
    expr = expr.replace("^", "**") # ** is used for pow in Python
    func = lambda x: eval(expr) # Assuming "x" is the independent var
    # Caution: Python uses j for sqrt(-1)

    #TODO Support for natural mathematic notation
    #TODO Input validation

    # A nested function because we're calling it multiple times within read_inputs
    def read_guess(guess_no): 
        # Reads one of the x values from the user

        prompt = f"Initial guess {guess_no}: " if not disable_prompts else ""
        x = input(prompt)
        """ 
        The complex() function returns a complex number when real and imaginary parts are provided,
        or it converts a string to a complex number; we're doing the latter here.
        """
        x = complex(x) 
        return x

    x0, x1, x2 = read_guess(0), read_guess(1), read_guess(2) # copying the return values to x0, x1, x2
    
    """ 
    The isclose function checks whether two values are close or not. 
    It is a bad practice to compare floats for equality due to implicit roundoffs.
    The real and imaginary parts are floats.
    """
    if isclose(x0, x1) or isclose(x1, x2) or isclose(x2, x0): 
        raise ValueError("At least two of the three guesses are the same.")

    return func, x0, x1, x2

def main(): 
    
    func, x0, x1, x2 = read_inputs(disable_prompts = DEBUG)

    for iteration_cnt in counting_forever(1): # counting_forever starts counting from 1

        x3 = find_next_guess(func, x0, x1, x2)

        # is all is required? Plus TODO ZeroDivisionError for x3

        """
        isclose will compare the absolute values of the two complex numbers.
        rel_tol is the relative tolerance. It is the maximum allowed difference between value x2 and x3. 
        In this case rel_tol = 0.001. This handles the work of calculating the relative percentage error.
        abs_tol is the minimum absolute tolerance. rel_tol doesn't work satisfactorily if one of x2 or x3 is 0.
        In this case abs_tol = 0.001 

        If x2 is almost equal to x3, no more iterations are required; x3 is the root.
        Otherwise if the no. of iterations have exceeded the earlier specified maximum,
        the loop must be halted.
        """
        if isclose(x2, x3, rel_tol = TOLERATED_PERCENTAGE_ERROR, abs_tol = TOLERATED_PERCENTAGE_ERROR)\
           or iteration_cnt >= MAX_ITERATIONS: 

            print(f"One of the roots is: {x3 : .4f}") # Setting precision 
            print(f"No. of iterations = {iteration_cnt}")
            print(f"Verification: f({x3}) = {func(x3)}") 
            # The latter number might get printed in scientific notation because it is so small.
            # Remember to look at the exponent following the number.
            break
            
        else:
            x0, x1, x2 = x1, x2, x3 # Including the newly found x3 as a guess.

# This makes our module importable from another program while still being able to be run on its own.
if __name__ == "__main__": main() 
