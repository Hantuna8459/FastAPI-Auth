from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from dotenv import set_key
import os

def generate_rsa_keys(env_file=".env"):
    # Check if the keys exist
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            if "PRIVATE_KEY" in f.read():
                print("Keys already exist. Skipping generation.")
                return

    # Generate the private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    # Generate the public key
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    # Save to .env
    set_key(env_file, "PRIVATE_KEY", private_key_pem.replace("\n", "\\n"))
    set_key(env_file, "PUBLIC_KEY", public_key_pem.replace("\n", "\\n"))

    print(f"Keys saved to {env_file}")

if __name__ == "__main__":
    generate_rsa_keys()
