import sys
from random import randint, randrange
from hashlib import sha256
from utils import curve, scalar_mult, point_add


def sign(msg, dA):
    s = 0
    r = 0
    if (len(sys.argv) > 1):
        msg = (sys.argv[1])
    # Alice's key pair (dA,QA)
        
    # Convert integer messages to strings
    if isinstance(msg, int):
        msg = str(msg)
        
    # Encode the input message to bytes using UTF-8 encoding
    encoded_msg = msg.encode('utf-8')
    
    # Calculate the hash of the encoded message using SHA-256
    h = int(sha256(encoded_msg).hexdigest(), 16)

    while s == 0:
        k = randint(1, curve.n - 1)
        rpoint = scalar_mult(k, curve.g)
        r = rpoint[0] % curve.n
        if r == 0:
            continue
        # Bob takes m and (r,s) and checks
        inv_k = pow(k, -1, curve.n)
        s = (inv_k * (h + r * dA)) % curve.n
    # print(f"Msg: {msg}\n\nAlice's private key={dA}\nAlice's public key={QA}\nk= {k}\n\nr={r}\ns={s}")
    return r, s


# To check signature
def verify(msg, r, s, QA):
    # Convert msg to bytes regardless of its type
    if isinstance(msg, str):
        msg_bytes = msg.encode('utf-8')
    elif isinstance(msg, int):
        msg_bytes = str(msg).encode('utf-8')
    else:
        msg_bytes = bytes(msg)
    # Calculate the hash of the encoded message using SHA-256
    h = int(sha256(msg_bytes).hexdigest(), 16)
    inv_s = pow(s, -1, curve.n)
    c = inv_s
    u1 = (h * c) % curve.n
    u2 = (r * c) % curve.n
    P = point_add(scalar_mult(u1, curve.g), scalar_mult(u2, QA))
    res = P[0] % curve.n
    if (res == r):
        print("- Signature matches!")
        return 1
    else:
        print("- Not Valid signature!!")
        return 0


def make_keypair():
    """Generates a random private-public key pair."""
    private_key = randrange(1, curve.n)
    public_key = scalar_mult(private_key, curve.g)

    return private_key, public_key