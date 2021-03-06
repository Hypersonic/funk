from funk import *

def naive_fib(n):
    ''' Naive fibonacci implementation
    '''
    if n <= 1: return 1
    return naive_fib(n-1) + naive_fib(n-2)

@precondition(lambda x: x >= 0)
@postcondition(lambda x: x > 0)
@match((0,), 1)
@match((1,), 1)
def fib_match(n):
    ''' Fibonacci function using direct pattern matching
    '''
    return fib_match(n-1) + fib_match(n-2)

@precondition(lambda x: x >= 0)
@postcondition(lambda x: x > 0)
@match_pred((lambda n: n <= 1,), 1)
def fib_pred(n):
    ''' Fibonacci using predicate-based pattern matching
    '''
    return fib_pred(n-1) + fib_pred(n-2)

@precondition(lambda x: x >= 0)
@postcondition(lambda x: x > 0)
@memoize
def fib_memo(n):
    ''' Memoized fibnacci
    '''
    if n <= 1: return 1
    return fib_memo(n-1) + fib_memo(n-2)

@precondition(lambda x: x >= 0)
@postcondition(lambda x: x > 0)
@lookup_table([0], [1], [10], [20], [30])
def fib_lookup(n):
    ''' Fibonacci with a lookup table for certain values
    '''
    if n <= 1: return 1
    return fib_lookup(n-1) + fib_lookup(n-2)


if __name__ == '__main__':
    print 'Naive:',naive_fib(10)
    print 'Pattern matching:',fib_match(10)
    print 'Predicate matching:',fib_pred(10)
    print 'Memoized:',fib_memo(10)
    print 'Lookup table:',fib_lookup(10)
