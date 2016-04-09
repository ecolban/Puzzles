'''
Two positive integers are chosen. The sum is revealed to logician A, and
the sum of squares is revealed to logician B. Both A and B are given this
information and the information contained in this sentence. The conversation
between A and B goes as follows. B starts

B: "I can't tell what they are."
A: "I can't tell what they are."
B: "I can't tell what they are."
A: "I can't tell what they are."
B: "I can't tell what they are."
A: "I can't tell what they are."
B: "Now I can tell what they are."

What are the two numbers?
When B first says that he cannot tell what the two numbers are, A receives
a large amount of information. But when A first says that he cannot tell
what the two numbers are, B already knows that A cannot tell what the two
numbers are. What good does it do B to listen to A?
'''


def memoize(f):
    memo = {}
    def h(*args):
        if not args in memo:
            memo[args] = f(*args)
        return memo[args]
    return h

def root(n):
    return int(n ** 0.5)

def decomp_sum(s):
    '''Returns a generator of all pairs (a, b) such that 1 <= a <= b and a + b == s'''
    return ((a, s - a) for a in xrange(1, s / 2 + 1))

@memoize
def decomp_sum_sq(s):
    '''Returns the list of all pairs (a, b) such that 1 <= a <= b and a**2 + b**2 == s'''
    return set((a, b) for a in xrange(1, root(s / 2) + 1)
                   for b in (root(s - a * a), )
                   if a * a + b * b == s)

def stmt_A(n, s):
    '''Predicate translating the n'th statement made by A, where s is the number revealed to A.'''
    set_A = set((a, b) for (a, b) in decomp_sum(s) if stmt_B(n, a * a + b * b))
    return len(set_A) > 1

def stmt_B(n, s):
    '''Predicate translating the n'th statement made by B, where s is the number revealed to B.'''
    set_B = decomp_sum_sq(s) if n == 1 else \
            set((a, b) for (a, b) in decomp_sum_sq(s) if stmt_A(n - 1, a + b))
    return len(set_B) > 1 if n < 4 else len(set_B) == 1
    

def check(a, b):
    '''Checks if (a, b) is a solution.'''
    sum_A, sum_B = a + b, a * a + b * b
    return stmt_B(1, sum_B) and\
           stmt_A(1, sum_A) and\
           stmt_B(2, sum_B) and\
           stmt_A(2, sum_A) and\
           stmt_B(3, sum_B) and\
           stmt_A(3, sum_A) and\
           stmt_B(4, sum_B)

def solution_gen():
    '''Returns a generator of all solutions in ascending order of their sums.'''
    s = 2
    while True:
        for (a, b) in decomp_sum(s):
            if check(a, b): yield(a, b)
        s += 1

solutions = solution_gen()
print('The first solution found is %s.' % str(next(solutions)))
print('The next solution is ...')
print('... %s' % str(next(solutions)))
    
       
                 
