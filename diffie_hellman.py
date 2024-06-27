import generate_prime as gp
import random
import hashlib
from ec_elgamal import sign, verify


def compute_shared_secret(private_key, other_public_key,p):
        return pow(other_public_key, private_key, p)

# derive a symmetric encryption key from the shared secret, first 16 bytes of a SHA256 hash
def compute_shared_key(shared_secret):
        return hashlib.sha256(str(shared_secret).encode()).digest()

def DH(ECaliceSecretKey,ECalicePublicKey,ECbobSecretKey,ECbobPublicKey):
        
        print("\n- Diffie Hellman exchange keys:\n")

        p = gp.generate_large_prime(512)  # generate a large prime number 

        #g = gp.primRoots(p) # generator function but it takes alot of time so we runned the code on g=2.
        g=2

        print(">>> Alice and Bob agreed on p(prime) and g(generator) values\n>>> Alice and Bob chose their private keys")

        DHalice_private_key=random.randint(1, p)
        DHbob_private_key=random.randint(1, p)

        print(">>> Alice and Bob computes their public key")

        DHalice_public_key=pow(g, DHalice_private_key, p)
        DHbob_public_key=pow(g, DHbob_private_key, p)

        r, s = sign(DHbob_public_key,ECbobSecretKey)

        print(">>> Alice and Bob both made their EC Elgamal secret key and public.")
        print(">>> Alice and Bob generated a a signature for their public keys using EC ElGamal")
        print(">>> Alice and Bob shared with each other their public keys and its digital signature")
        print(">>> Alice and Bob verified each other digital signature using EC ElGamal")
        #verify
        veri=verify(DHbob_public_key, r, s,ECbobPublicKey)

        if veri == 1:   
            alice_shared_K = compute_shared_secret(DHalice_private_key,DHbob_public_key,p)
        else:
             print("Unverified public key for alice cant compute bob shared key.")
             exit(0)

        #Alice send to Bob public key with signature
        r, s = sign(DHalice_public_key,ECaliceSecretKey)

        #verify
        #Bob verify the public key of Alice
        veri=verify(DHalice_public_key, r, s,ECalicePublicKey)

        if veri == 1:   
             bob_shared_K = compute_shared_secret(DHbob_private_key,DHalice_public_key,p)
        else:
             print("Unverified public key for alice cant compute bob shared key.")
             exit(0)

        alice_key = compute_shared_key(alice_shared_K)
        bob_key = compute_shared_key(bob_shared_K)

        print(">>> Alice and Bob computed their shared key")

        assert alice_shared_K == bob_shared_K, "Keys do not match."
        return alice_key,bob_key,
      
