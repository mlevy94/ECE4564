from md5auth import createMD5, authMD5

mystring = input("input test string: ")
myhash = createMD5(mystring)
print (mystring, myhash)
success = authMD5(myhash, mystring)
if(success):
    print("success!")
else:
    print("failure")
    
