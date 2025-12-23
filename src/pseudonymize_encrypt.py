import mysql.connector, pandas as pd, uuid, json, base64, secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chethu@1234",
    database="clinical_trial"
)

df = pd.read_sql("SELECT * FROM patients", conn)

# Load RSA public key
with open("keys/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

def encrypt_field(value, aes, pseudonym):
    nonce = secrets.token_bytes(12)
    ciphertext = aes.encrypt(
        nonce,
        str(value).encode(),
        pseudonym.encode()
    )
    return {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }

secure_store = []
safe_data = []

for _, row in df.iterrows():
    pseudonym = str(uuid.uuid4())

    aes_key = secrets.token_bytes(32)
    aes = AESGCM(aes_key)

    wrapped_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    encrypted_fields = {
        "name": encrypt_field(row["name"], aes, pseudonym),
        "dob": encrypt_field(row["dob"], aes, pseudonym),
        "ssn": encrypt_field(row["ssn"], aes, pseudonym),
        "lab_results": encrypt_field(row["lab_results"], aes, pseudonym)
    }

    secure_store.append({
        "pseudonym": pseudonym,
        "wrapped_key": base64.b64encode(wrapped_key).decode(),
        "encrypted_fields": encrypted_fields
    })

    safe_data.append({
        "pseudonym": pseudonym,
        "diagnosis": row["diagnosis"],
        "treatment": row["treatment"]
    })

pd.DataFrame(safe_data).to_csv("output/pseudonymized_dataset.csv", index=False)

with open("output/secure_store.json", "w") as f:
    json.dump(secure_store, f, indent=4)

conn.close()
print("✅ Pseudonymization + Encryption completed correctly")
