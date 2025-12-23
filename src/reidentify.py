import json, base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Load private key
with open("keys/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Load secure store
with open("output/secure_store.json", "r") as f:
    secure_data = json.load(f)

print("\n🔓 FULL RE-IDENTIFICATION (AUTHORIZED)\n")

for i, record in enumerate(secure_data, start=1):

    # Decrypt AES key
    aes_key = private_key.decrypt(
        base64.b64decode(record["wrapped_key"]),
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    aes = AESGCM(aes_key)

    print(f"Patient {i}")
    print(f"  Pseudonym : {record['pseudonym']}")

    # Decrypt ALL encrypted fields
    for field, enc in record["encrypted_fields"].items():
        value = aes.decrypt(
            base64.b64decode(enc["nonce"]),
            base64.b64decode(enc["ciphertext"]),
            record["pseudonym"].encode()   # AAD
        ).decode()

        print(f"  {field.capitalize():12}: {value}")

    print("-" * 45)
