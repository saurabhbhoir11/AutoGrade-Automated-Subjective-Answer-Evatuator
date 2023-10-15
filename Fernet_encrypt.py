from cryptography.fernet import Fernet

with open("encryption_key.key", "rb") as key_file:
    key = key_file.read()


def decrypt_file(encrypted_file_path, key):
    cipher_suite = Fernet(key)
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = cipher_suite.encrypt(encrypted_data)
    with open(encrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

encrypted_file = "creds.json"
decrypt_file(encrypted_file, key)
