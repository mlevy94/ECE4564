import hashlib

def createMD5(inString):
    m = hashlib.md5()
    m.update(inString)
    return m.hexdigest()

def authMD5(inString, inHash)
    m = hashlib.md5()
    m.update(instring)

    if (inHash == m.hexdigest())
        return True
    return False


