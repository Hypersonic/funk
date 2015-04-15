from functools import wraps

def match(matches, result):
    ''' Match arguments of tuple matches and return result when they are used
        If there is not a match, call the function

        You cannot match kwargs

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

        You cannot match on kwargs

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
                raise ValueError("Precondition not met on function %s!"%f.func_name)
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
                raise ValueError("Postcondition not met on function %s!"%f.func_name)
        return inner
    return decorator

def memoize(f):
    ''' Memoize a function by caching the return values of any calls
        Arguments must be hashable (ie, usable as a dict key)

        If the function is impure, this may return unexpected results

        Does not work on functions that require kwargs
    '''
    cache = {}
    @wraps(f)
    def inner(*args):
        if not args in cache:
            value = cache[args] = f(*args)
        else: value = cache[args]
        return value
    return inner

def lookup_table(*lookups):
    ''' Create a lookup table that gets checked before the function
        gets actually called.
        The results of the lookup are generated as the function is first called
        by running the function for each lookup value.
    '''
    def decorator(f):
        table = {}
        # we have to use a list so table_generated
        # won't get shadowed when we try to assign to it
        table_generated = [False]
        @wraps(f)
        def inner(*args, **kwargs):
            # Generate the lookup table on the first call
            if not table_generated[0]:
                # switch now so we don't infinitely
                # bounce back in recursive functions
                table_generated[0] = True
                for lookup in lookups:
                    table[tuple(lookup)] = f(*lookup)

            if args in table:
                return table[args]
            else:
                return f(*args, **kwargs);
        return inner
    return decorator
