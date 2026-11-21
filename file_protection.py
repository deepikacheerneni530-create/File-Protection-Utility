import os
from pathlib import Path
from getpass import getpass

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

# Security settings
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
ITERATIONS = 600000
MAGIC = b"FPU1"


# Generate encryption key using PBKDF2
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS
    )
    return kdf.derive(password.encode("utf-8"))


# Encrypt a file
def encrypt_file(filename, password):
    file_path = Path(filename)

    if not file_path.is_file():
        print("Error: File not found!")
        return

    data = file_path.read_bytes()

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    key = generate_key(password, salt)
    aes = AESGCM(key)

    ciphertext = aes.encrypt(nonce, data, None)

    output_file = Path(str(file_path) + ".enc")

    output_file.write_bytes(
        MAGIC + salt + nonce + ciphertext
    )

    print("\nFile encrypted successfully!")
    print("Encrypted file:", output_file)


# Decrypt a file
def decrypt_file(filename, password):
    file_path = Path(filename)

    if not file_path.is_file():
        print("Error: Encrypted file not found!")
        return

    encrypted_data = file_path.read_bytes()

    header_size = len(MAGIC) + SALT_SIZE + NONCE_SIZE

    if (len(encrypted_data) < header_size + 16
            or not encrypted_data.startswith(MAGIC)):
        print("Error: Invalid encrypted file!")
        return

    salt_start = len(MAGIC)
    nonce_start = salt_start + SALT_SIZE

    salt = encrypted_data[salt_start:nonce_start]
    nonce = encrypted_data[nonce_start:header_size]
    ciphertext = encrypted_data[header_size:]

    key = generate_key(password, salt)
    aes = AESGCM(key)

    try:
        plaintext = aes.decrypt(nonce, ciphertext, None)

        output_file = file_path.with_name(
            file_path.name[:-4] + "_decrypted"
        )

        output_file.write_bytes(plaintext)

        print("\nFile decrypted successfully!")
        print("Recovered file:", output_file)

    except InvalidTag:
        print("\nDecryption failed!")
        print("Wrong password or file has been modified.")


# Main menu
def main():
    while True:
        print("\n===== FILE PROTECTION UTILITY =====")
        print("1. Encrypt File")
        print("2. Decrypt File")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            filename = input("Enter file name: ")
            password = getpass("Enter password: ")

            if not password:
                print("Password cannot be empty!")
                continue

            encrypt_file(filename, password)

        elif choice == "2":
            filename = input("Enter encrypted file name: ")
            password = getpass("Enter password: ")

            if not password:
                print("Password cannot be empty!")
                continue

            decrypt_file(filename, password)

        elif choice == "3":
            print("Thank you for using File Protection Utility!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()