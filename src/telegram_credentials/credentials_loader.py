from cryptography.fernet import Fernet

def readBytesFromFile(filepath: str) -> bytes:
    with open(filepath, 'rb') as f:
        msg = f.read()
    f.close()
    return msg

def loadCredentialsIntoDictionary(credentialsString: str) -> dict[str, str]:
    credList = credentialsString.split("\n")
    credMap = dict()
    for cred in credList:
        keyValue = cred.split(": ", 1)
        if len(keyValue) < 2:
            continue
        key, value = keyValue
        credMap[key] = value
    return credMap

def readCredentials(pathToKey: str, pathToCredentials: str) -> str:
    key = readBytesFromFile(pathToKey)
    encCredentials = readBytesFromFile(pathToCredentials)

    fernet = Fernet(key)
    credentials = fernet.decrypt(encCredentials).decode()
    return credentials

def getCredentialsMap(pathToKey: str, pathToCredentials: str) -> dict[str, str]:
    credentials = readCredentials(pathToKey, pathToCredentials)
    return loadCredentialsIntoDictionary(credentials)
