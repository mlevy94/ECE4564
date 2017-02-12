import hashlib

def createMD5(inString):
    hashList = []
    m = hashlib.md5()
    if isinstance(inString, (tuple,list)):
        for entry in inString:
            m.update(entry.encode())
            hashList.append(m.hexdigest())
        return hashList
    else:
        m.update(inString.encode())
        return m.hexdigest()

def authMD5(inHash, inString):
    hashList = []
    m = hashlib.md5()
    for entry, verHash in zip(inString, inHash):
        m.update(entry.encode())
        if m.hexdigest() != verHash:
                return False
    return True


