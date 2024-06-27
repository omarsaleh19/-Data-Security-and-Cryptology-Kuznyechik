import random
from math import gcd as bltin_gcd

# verify if a number is likely prime by performing k-number of Miller-Rabin primality tests:
# Let n > 2 be an odd integer and write n - 1 = 2^s * d with d odd. If there is an integer a such that either
# a^d ≡ 1 (mod n), or
# a^(2^r * d) ≡ -1 (mod n) for some 0 <= r < s
# then n is said to be a strong pseudoprime to the base a.
def check_prime(n, k=5):  # number of Miller-Rabin tests
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# perform a loop generating a pseudorandom int with k random bits, checking with Miller-Rabin primality tests
def generate_large_prime(bits=512):  # length in bits
    while True:
        probable_prime = random.getrandbits(bits)
        probable_prime |= (1 << bits - 1) | 1  # set first and last bits to ensure the probable prime is odd and of correct bit length
        if check_prime(probable_prime):
            return probable_prime
        
def primRoots(_inprime):
    required_set = {num for num in range(1, _inprime) if bltin_gcd(num, _inprime) }
    return [g for g in range(1, _inprime) if required_set == {pow(g, powers, _inprime)
            for powers in range(1, _inprime)}]
