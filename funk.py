from functools import wraps

def match(matches, result):
    ''' Match arguments of tuple matches and return result when they are used
        If there is not a match, call the function

        WARNING: With single item tuples, you must put a comma
        after the item, or it is interpreted as a pair of parens
    '''
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if args == matches:
                return result
            return f(*args, **kwargs)
        return inner
    return decorator

def match_pred(matches, result):
    ''' Match arguments who return True when passed into their corresponding
        element in tuple matches and return result when they are used

        Elements that are None will act as if they always return True

        If there is not a match, call the function

        WARNING: With single item tuples, you must put a comma
        after the item, or it is interpreted as a pair of parens
    '''
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if all(match is None or match(arg) for match, arg in zip(matches, args)):
                return result
            return f(*args, **kwargs)
        return inner
    return decorator

def precondition(pred):
    ''' Require that a predicate on the arguments be matched in order
        for the function to be called.

        Raises a ValueError if not
    '''
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if pred(*args, **kwargs):
                return f(*args, **kwargs)
            else:
                raise ValueError("Precondition not met!")
        return inner
    return decorator

def postcondition(pred):
    ''' Require that a predicate on the return value to 
        be matched in order for the function to return.

        Raises a ValueError if not
    '''
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            result = f(*args, **kwargs)
            if pred(result):
                return result
            else:
                raise ValueError("Postcondition not met!")
        return inner
    return decorator

@precondition(lambda x: x >= 0)
@postcondition(lambda x: x > 0)
@match((0,), 1)
@match((1,), 1)
def fib_match(n):
    ''' Fibonacci function using direct pattern matching
    '''
    return fib_match(n-1) + fib_match(n-2)

@match_pred((lambda n: n <= 1,), 1)
def fib_pred(n):
    ''' Fibonacci using predicate-based pattern matching
    '''
    return fib_pred(n-1) + fib_pred(n-2)


if __name__ == '__main__':
    print fib_match(10)
    print fib_pred(10)
