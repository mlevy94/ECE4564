import hashlib

def createMD5(inString):
    m = hashlib.md5()
    m.update(inString.encode())
    return m.hexdigest()

def authMD5(inHash, inString):
    m = hashlib.md5()
    m.update(inString.encode())

    if (inHash == m.hexdigest()):
        return True
    return False


