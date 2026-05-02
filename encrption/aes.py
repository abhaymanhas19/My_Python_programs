import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# AESGCM
# Symmetric authenticated encryption: provides confidentiality + integrity.

data_to_encrypt = "hello My name is abh ay"

key = AESGCM.generate_key(bit_length=256)
print(key)
aesgcm = AESGCM(key)

nonce = os.urandom(14)

print("nonce          :", nonce)
ciphertext = aesgcm.encrypt(nonce, data_to_encrypt.encode(), associated_data=None)

print("key       :", base64.urlsafe_b64encode(key).decode())
print("nonce     :", base64.urlsafe_b64encode(nonce).decode())
print("ciphertext:", base64.urlsafe_b64encode(ciphertext).decode())


decrypted = aesgcm.decrypt(nonce, ciphertext, associated_data=None).decode()
print("decrypted :", decrypted)
