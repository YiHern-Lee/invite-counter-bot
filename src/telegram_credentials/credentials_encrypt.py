from cryptography.fernet import Fernet
import os

### Script to encrypt a message ###

# Stores the message to be encrypted
# Message should be in format "<key>: <value>" and each key-value pair should be in a new line
message = """
telegram-bot-api-key: <telegram-bot-api-key>

"""

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# Generate a new key to encrypt message
key = Fernet.generate_key()

# Path to write key and credentials
pathToKey = CURRENT_PATH + "/key.txt"
pathToCredentials = CURRENT_PATH + "/../../credentials.txt"

# Writes the encryption key to current directory
with open(pathToKey, "wb") as keyFile:
    keyFile.write(key)
keyFile.close()

fernet = Fernet(key)

encMessage = fernet.encrypt(message.encode())

# Writes the encrypted message to the file path specified
with open(pathToCredentials, "wb") as credFile:
    credFile.write(encMessage)
credFile.close()
