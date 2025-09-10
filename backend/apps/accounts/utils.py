import random


# -----------------------------------------------------------------------------
def create_random_code(count):
    count -= 1
    return random.randint(10**count, 10 ** (count + 1) - 1)
