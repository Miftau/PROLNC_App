from cryptography.fernet import Fernet

# Generate the key
key = Fernet.generate_key()

# Print the key (you can save it to a file for later use)
print(f"Generated Fernet Key: {key}")

# You can save the key to a file to reuse it later
with open('fernet.key', 'wb') as key_file:
    key_file.write(key)
