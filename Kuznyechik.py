import os
import boxes as b


# The input x and the output y have 128-bits
def S(x):
	y = 0
	for i in reversed(range(16)):
		y <<= 8
		y ^= b.pi[(x >> (8 * i)) & 0xff]
	return y


# The input x and the output y have 128-bits
def S_inv(x):
	y = 0
	for i in reversed(range(16)):
		y <<= 8
		y ^= b.pi_inv[(x >> (8 * i)) & 0xff]
	return y


# x and y are nonnegative integers 
# Their associated binary polynomials are multiplied. 
# The associated integer to this product is returned. 
def multiply_ints_as_polynomials(x, y):
	if x == 0 or y == 0:
		return 0
	z = 0
	while x != 0:
		if x & 1 == 1:
			z ^= y
		y <<= 1
		x >>= 1
	return z


# Returns the number of bits that are used 
# to store the positive integer integer x.
def number_bits(x):
	nb = 0
	while x != 0:
		nb += 1
		x >>= 1
	return nb


# x is a nonnegative integer
# m is a positive integer
def mod_int_as_polynomial(x, m):
	nbm = number_bits(m)
	while True:
		nbx = number_bits(x) 
		if nbx < nbm:
			return x
		mshift = m << (nbx - nbm)
		x ^= mshift


# x,y are 8-bits
# The output value is 8-bits
def kuznyechik_multiplication(x, y):
	z = multiply_ints_as_polynomials(x, y)
	m = int('111000011', 2)
	return mod_int_as_polynomial(z, m)


# The input x is 128-bits (considered as a vector of sixteen bytes)
# The return value is 8-bits
def kuznyechik_linear_functional1(x):
	C = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1] 
	y = 0
	while x != 0:
		y ^= kuznyechik_multiplication(x & 0xff, C.pop())
		x >>= 8
	return y

def kuznyechik_linear_functional(x):
    C = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]
    y = 0
    while x != 0 and C:
        y ^= kuznyechik_multiplication(x & 0xff, C.pop())
        x >>= 8
    return y



# The input value x and the output value is 128-bits
def R(x):
	a = kuznyechik_linear_functional(x)
	return (a << 8 * 15) ^ (x >> 8)


# The input value x and the output value are 128-bits
def R_inv(x):
	a = x >> 15 * 8
	x = (x << 8) & (2 ** 128 - 1)
	b = kuznyechik_linear_functional(x ^ a)
	return x ^ b


# The input value x and the output value is 128-bits
# This function is the composition of R sixteen times
def L(x):
	for _ in range(16):
		x = R(x)
	return x


# The input value x and the output value are 128-bits
def L_inv(x):
	for _ in range(16):
		x = R_inv(x)
	return x


# k is 256-bits
# The key schedule algorithm returns 10 keys of 128-bits each
def kuznyechik_key_schedule1(k):
	keys = [] 
	a = k >> 128
	b = k & (2 ** 128 - 1)
	keys.append(a)
	keys.append(b)
	for i in range(4):
		for j in range(8):
			c = L(8 * i + j + 1)
			(a, b) = (L(S(a ^ c)) ^ b, a) 
		keys.append(a)
		keys.append(b)
	return keys

def kuznyechik_key_schedule(k):
    k_int = int.from_bytes(k, byteorder='big')  # Convert bytes to integer
    keys = [] 
    a = k_int >> 128
    b = k_int & (2 ** 128 - 1)
    keys.append(a)
    keys.append(b)
    for i in range(4):
        for j in range(8):
            c = L(8 * i + j + 1)
            (a, b) = (L(S(a ^ c)) ^ b, a) 
        keys.append(a)
        keys.append(b)
    return keys


# The plaintext x is 128-bits
# The key k is 256-bits 
def encryption(x, k):
	keys = kuznyechik_key_schedule(k)
	for round in range(9):
		x = L(S(x ^ keys[round]))
	return x ^ keys[-1]


# The ciphertext x is 128-bits
# The key k is 256-bits 
def decryption(x, k):
	keys = kuznyechik_key_schedule(k)
	keys.reverse()
	for round in range(9):
		x = S_inv(L_inv(x ^ keys[round]))
	return x ^ keys[-1]

