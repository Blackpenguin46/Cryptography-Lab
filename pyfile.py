from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


# Function to encrypt a plaintext message and write it to a file
def encrypt_message_to_file(plaintext, output_file):
    key = os.urandom(32)  # Generate a random 32-byte key for AES-256
    iv = os.urandom(16)  # Generate a random 16-byte Initialization Vector (IV)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to ensure it's a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Write the key, IV, and ciphertext to the output file
    with open(output_file, 'wb') as f:
        f.write(key + iv + ciphertext)


# Function to decrypt the ciphertext from a file and return the original plaintext
def decrypt_message_from_file(encrypted_file):
    with open(encrypted_file, 'rb') as f:
        data = f.read()

    key = data[:32]  # Extract the first 32 bytes as the key
    iv = data[32:48]  # Extract the next 16 bytes as the IV
    ciphertext = data[48:]  # The rest is the ciphertext

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode()  # Return the original plaintext as a string


# Main execution
plaintext = input("Enter a message to encrypt: ")
output_file = "encrypted_message.bin"  # Specify the output file for encrypted message

# Encrypt the plaintext message and save it to the file
encrypt_message_to_file(plaintext, output_file)
print("Message encrypted successfully and saved to", output_file)

# Decrypt the message from the file
decrypted_message = decrypt_message_from_file(output_file)
print("Decrypted message:", decrypted_message)
