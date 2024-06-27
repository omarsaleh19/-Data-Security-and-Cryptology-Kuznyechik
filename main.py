import diffie_hellman as dh
from ec_elgamal import sign, verify, make_keypair
import random
import cbc

# alice sends encrypted message to Bob

message="Hello Bob how are you today? ,Are you ready for the presentation?"

print("\n- Alice want to send this SMS message to Bob: ",message)

#EC Elgamal Signature -- Keys
aliceSecretKey, alicePublicKey = make_keypair()
bobSecretKey, bobPublicKey = make_keypair()

Alice_key,Bob_key=dh.DH(aliceSecretKey,alicePublicKey,bobSecretKey,bobPublicKey)

iv =(random.getrandbits(128))
iv='{:032x}'.format(iv)

print("\n>>> Alice wrote a message:",message)

#sign
r, s = sign(message, aliceSecretKey)
print("- Message signed by alice using her EC elgamal private key..")

print(">>> Alice generated initial vector (IV) for CBC")

print(">>> Alice encypting the message using Kuznyechik in CBC mode with Alice key and IV...")
encrypted_hexa=cbc.encrypt2(message,Alice_key,iv)

print("- The cipher text:\n\n", encrypted_hexa)

print("\n>>> Alice shared the ciphertext, IV, digital signature with BOB...")

print(">>> Bob recieved them from Alice")

decrypted_message = cbc.decrypt2(encrypted_hexa, Bob_key,iv) # we use the same iv Alice used.

print(">>> Bob decrypted the ciphertext using Kuznyechik in CBC mode")

original_message = decrypted_message.decode('utf-8')

print("- The decrypted message:",original_message)

ver = verify(original_message, r, s,alicePublicKey)
if ver == 1 :
    print(">>> Message is verfied by bob")
else:
    exit(0)

# check that the decrypted message is the same as the original message
assert original_message == message, "- Decrypted messages don't match"
