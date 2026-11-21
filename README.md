File Protection Utility

Project Description

File Protection Utility is a Python-based cybersecurity project that protects sensitive files using AES-256 encryption and decryption.

Objectives

- Encrypt files using AES-256-GCM.
- Generate secure encryption keys using PBKDF2.
- Protect files using password-based authentication.
- Decrypt encrypted files using the correct password.
- Detect incorrect passwords and modified encrypted files.

Technologies Used

- Python
- AES-256-GCM
- PBKDF2
- Cryptography Library
- Visual Studio Code

Project Files

- "file_protection.py" – Main Python program.
- "sample.txt" – Sample input file.
- "sample.txt.enc" – Encrypted file.
- "sample.txt_decrypted" – Decrypted output file.
- "README.md" – Project documentation.

Installation

Install the required library:

py -m pip install cryptography

How to Run

py file_protection.py

Features

1. File encryption.
2. File decryption.
3. Password-based key generation.
4. Incorrect password detection.
5. File integrity verification.

Testing

- Successful encryption.
- Successful decryption.
- Incorrect password rejection.
- Original and decrypted file comparison using SHA-256.

Conclusion

This project demonstrates how Python cryptography techniques can be used to protect sensitive files from unauthorized access.