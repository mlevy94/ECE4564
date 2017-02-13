import hashlib

# createMD5
# @breif	Creates a list of md5 hashes given a list of input strings
# @param	inString	A list or tuple of input strings
# @return	hashlist	A list of md5 hashes corresponding to input strings
def createMD5(inString):
    hashList = []
    m = hashlib.md5()
    if isinstance(inString, (tuple,list)):
        for entry in inString:		#create a list of md5 hashes
            m.update(entry.encode())
            hashList.append(m.hexdigest())
        return hashList
    else:#no strings allowed, must be list of strings
        raise Exception("Input must be a list or tuple")

# authMD5 
# @breif	Verifies a list of strings given a list of hashes. Returns true
#			when all strings match the given hashes, or false otherwise
# @param	inHash		A list of hashes to test
# @param	inString	A list of strings to verify
# @retval	True		Strings successfully authenticated
# @retval	False		Authentication failed
def authMD5(inHash, inString):
    hashList = []
    m = hashlib.md5()
    for entry, verHash in zip(inString, inHash):
        m.update(entry.encode())
        if m.hexdigest() != verHash:
                return False
    return True


