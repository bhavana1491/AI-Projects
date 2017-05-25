from itertools import chain

x = [('Edgar','A'), ('Robert','B')]

# list is to materialize the entire sequence.
# Normally you would use this in a for loop with no `list()` call.
print list(chain.from_iterable(x))