import hashlib

print("=== Password Hashing Demo ===")

password = input("Enter a password: ")

# MD5 (weak)
md5_hash = hashlib.md5(password.encode()).hexdigest()

# SHA256 (stronger)
sha256_hash = hashlib.sha256(password.encode()).hexdigest()

print("\n[+] MD5 Hash (INSECURE):")
print(md5_hash)

print("\n[+] SHA256 Hash (BETTER):")
print(sha256_hash)

print("\n⚠️ Same password always gives same hash!")

