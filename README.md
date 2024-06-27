
# -📱🔒 Secure SMS Exchange Application
This application provides secure SMS exchange by leveraging:

🛡 Encryption-Decryption with Kuznyechik in CBC Mode: Ensures that your messages are securely encrypted and decrypted using the robust Kuznyechik algorithm in Cipher Block Chaining (CBC) mode.

🔑 Diffie-Hellman (DH) Key Generation: Implements secure key exchange using the Diffie-Hellman protocol, ensuring that your keys are exchanged safely and confidentially.

✍️ Signature with EC ElGamal: Utilizes Elliptic Curve ElGamal for digital signatures, adding an additional layer of security by verifying the authenticity and integrity of your messages.

🧩 Components
Kuznyechik: A symmetric block cipher with a block size of 128 bits and a key length of 256 bits.
Cipher Block Chaining (CBC): A mode of operation for a block cipher.
ElGamal Signature Scheme: A digital signature scheme based on the algebraic properties of modular exponentiation and the discrete logarithm problem.
Elliptic Curve Cryptography (ECC): An approach to public-key cryptography based on the algebraic structure of elliptic curves over finite fields.
🔑 Key Exchange
To resolve key exchange in the symmetric algorithm, we use Diffie-Hellman (DH), a mathematical method for securely exchanging cryptographic keys over a public channel. To ensure no tampering, Alice and Bob attach digital signatures using EC ElGamal to their public keys for verification.

🔒 Encryption
Check KEY: Must be 256-bit.
Text: Partition the text into 128-bit blocks. If the last block is less than 128-bit, add ‘1’ and pad with zeroes to 128-bit.
CBC Mode: Loop on the blocks and encrypt each using Kuznyechik.
Concatenate: All ciphertext blocks into one string and return.
🔓 Decryption
Check KEY: Must be 256-bit.
Text: Partition the text into 128-bit blocks.
Decrypt: Each block using Kuznyechik and CBC mode.
✍️ Digital Signature
Alice generates a digital signature on her message using EC ElGamal, and Bob verifies it after decryption to ensure message integrity.

🔄 Project Flow
Alice and Bob use Diffie-Hellman to exchange keys and compute a shared key.
They agree on (p, g) values, choose private keys, compute public keys, generate and share signatures using EC ElGamal.
Alice writes and encrypts a message, then shares ciphertext, IV, and signature with Bob.
Bob decrypts the ciphertext and verifies the signature.
📝 Conclusions
This application combines Kuznyechik encryption in CBC mode, Diffie-Hellman key exchange, and EC ElGamal signature to ensure secure communication and data protection, providing robust encryption, decryption, and secure key delivery.
