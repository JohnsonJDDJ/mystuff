# part of the code is written by ChapGPT
# chat.openai.com

import sys

def encrypt(message, key):
    '''Encryption with private key'''
    # Convert the message and key into a series 
    # of numbers using the ASCII codes
    message_numbers = [ord(c) for c in message]
    key_numbers = [ord(c) for c in key]

    # Repeat the key if it is shorter than the message
    while len(key_numbers) < len(message_numbers):
        key_numbers += key_numbers

    # Perform the XOR operation on each pair 
    # of numbers and add 32 to avoid unprintable characters
    encrypted_numbers = [m ^ k for m, k in zip(message_numbers, key_numbers)]
    encrypted_numbers = [i + 32 for i in encrypted_numbers]

    # Convert the encrypted numbers back into 
    # characters and return the encrypted message
    return "".join([chr(n) for n in encrypted_numbers])

def decrypt(message, key):
    '''Decryption with private key'''
    # Convert the message and key into a series 
    # of numbers using the ASCII codes
    message_numbers = [ord(c) - 32 for c in message]
    key_numbers = [ord(c) for c in key]

    # Repeat the key if it is shorter than the message
    while len(key_numbers) < len(message_numbers):
        key_numbers += key_numbers

    # Perform the XOR operation on each pair 
    # of numbers (one from the message and one from the key)
    decrypted_numbers = [m ^ k for m, k in zip(message_numbers, key_numbers)]

    # Convert the decrypted numbers back into 
    # characters and return the decrypted message
    return "".join([chr(n) for n in decrypted_numbers])


if __name__ == "__main__":
    type = sys.argv[1]
    if type == "E":
        message = input("Message: ")
        key = input("Key: ")
        print(f"<{encrypt(message, key)}> (encryption inside the bracket)")
    elif type == "D":
        message = input("Message: ")
        key = input("Key: ")
        print(f"<{decrypt(message, key)}> (decryption inside the bracket)")
    else:
        raise TypeError("Invalid argument. D for decrypt, E for encrypt.")