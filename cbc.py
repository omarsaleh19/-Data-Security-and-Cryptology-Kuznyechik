import Kuznyechik

"""
parameter : ptext - string , key - hex ,iv- hex 64bit
return ctext-hex
"""

def split_plaintext_to_hex_blocks(plaintext):
    lengthB=0
    blocks_list = []
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i + 16]
        if len(block) < 16:
            c = 16 - len(block)
            for i in range(c):
                if c==0:
                    block=block+"1"
                block = block + "\0"
        blocks_list.append(block)
    return lengthB,blocks_list


def encrypt2(message, key, iv):
    # Split the message into blocks of length 16 (128 bits)We know if len ( message ) % 16 != 0 
    # the last block will not be with length of 16 but the compiler will do it automaticly
    #blocks = [message[i:i+16] for i in range(0, len(message), 16)]
    lengthB,blocks=split_plaintext_to_hex_blocks(message)
    # Convert the initialization vector (iv) to bytes
    iv_bytes = bytes.fromhex(iv)

    # Convert the IV bytes to an integer
    previous = int.from_bytes(iv_bytes, byteorder='big')

    encrypted_blocks = []
    for block in blocks:
        # Convert the current block to bytes
        block_bytes = block.encode()
        # XOR operation
        xor_block = int.from_bytes(block_bytes, byteorder='big') ^ previous

        # Encryption using the key 
        encrypted_block = Kuznyechik.encryption(xor_block, key)

        # Convert the encrypted block back to bytes
        encrypted_block_bytes = encrypted_block.to_bytes((encrypted_block.bit_length() + 7) // 8, byteorder='big')

        # Update the previous block for the next iteration
        previous = encrypted_block

        encrypted_blocks.append(encrypted_block_bytes)

    return b''.join(encrypted_blocks)





def decrypt2(ctext, key, iv):
    # Split the ciphertext into blocks of length 16 (128 bits) We know if len ( ctext ) % 16 != 0 
    # the last block will not be with length of 16 but the compiler will do it automaticly
    #blocks = [ctext[i:i+16] for i in range(0, len(ctext), 16)]
    lengthB,blocks=split_plaintext_to_hex_blocks(ctext)
    # Convert the initialization vector (iv) to bytes
    iv_bytes = bytes.fromhex(iv)

    # Convert the IV bytes to an integer
    previous = int.from_bytes(iv_bytes, byteorder='big')

    decrypted_blocks = []
    for block in blocks:
        # Convert the current block to an integer
        block_int = int.from_bytes(block, byteorder='big')

        # Decryption using the key
        decrypted_block = Kuznyechik.decryption(block_int, key)

        # XOR operation
        xor_block = decrypted_block ^ previous

        # Convert the XOR result back to bytes
        decrypted_block_bytes = xor_block.to_bytes((xor_block.bit_length() + 7) // 8, byteorder='big')

        # Update the previous block for the next iteration
        previous = block_int

        decrypted_blocks.append(decrypted_block_bytes)


    plaintext = b''.join(decrypted_blocks).rstrip(b'\0')
    return plaintext