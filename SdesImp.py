#key generation
p10=[3,5,2,7,4,10,1,9,8,6]
p8=[6,3,7,4,8,5,10,9]
ip=[2,6,3,1,4,8,5,7]
ep=[4,1,2,3,2,3,4,1]
p4=[2,4,3,1]
ipinverse=[4,1,3,5,7,2,8,6]
s0=[[1,0,3,2],
    [3,2,1,0],
    [0,2,1,3],
    [3,1,3,2]]
s1=[[0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3]]
def permutate_key(key,p10):
    new_key=[]
    for i in range(len(p10)):
        value= key[p10[i]-1]
        #print(value)
        new_key.append(value)
        #print(new_key)
    return new_key
def left_shift(key,bit):
    leftShiftBits=[]
    for i in range(len(key)):
        value=key[(i+bit)%len(key)]
        leftShiftBits.append(value)
    return leftShiftBits
def xor_func(ep,key):
    xorout=[]
    for i in range(len(key)):
        out=(ep[i]+key[i])%2
        xorout.append(out)
    return xorout
def read_s0(xoroutput,sbox):
    firstfourbit=xoroutput[:4]
    lastfourbit=xoroutput[4:]
    if(firstfourbit[0]==1):
        row=(firstfourbit[0]*2)+firstfourbit[3]
    else:
        row=firstfourbit[0]+firstfourbit[3]
    if(firstfourbit[1]==1):
        column=(firstfourbit[1]*2)+firstfourbit[2]
    else:
        column=firstfourbit[1]+firstfourbit[2]
    val=sbox[row][column]
    return val
def read_s1(xoroutput,sbox):
    #firstfourbit=xoroutput[:4]
    lastfourbit=xoroutput[4:]
    if(lastfourbit[0]==1):
        row=(lastfourbit[0]*2)+lastfourbit[3]
    else:
        row=lastfourbit[0]+lastfourbit[3]
    if(lastfourbit[1]==1):
        column=(lastfourbit[1]*2)+lastfourbit[2]
    else:
        column=lastfourbit[1]+lastfourbit[2]
    val=sbox[row][column]
    return val

def dec_to_bin(val):
    temp=val
    binary=[]
    while (val>0):
        rem=val%2
        binary.append(rem)
        val=val//2
    if(temp==1):
        binary.append(0)
    if(temp==0):
        binary.append(0)
        binary.append(0)
    return binary[::-1]




#end function
#key=[0,1,1,1,1,1,1,1,0,1]
print("input the 10 bit key")
key=[]
for i in range(10):
    element=int(input())
    key.append(element)
#key_in = input('10 bit key: ')
permutatedkey=permutate_key(key,p10)
print("below is the p10 of key")
print(permutatedkey)
leftshift1=left_shift(permutatedkey[:5],1)+left_shift(permutatedkey[5:],1)
print("below after left shift by 1 bit ")
print(leftshift1)
key1=permutate_key(leftshift1,p8)
#print(key1)
leftshift2=left_shift(leftshift1[:5],2)+left_shift(leftshift1[5:],2)
print("below after left shift by 2 bit ")
print(leftshift2)
key2=permutate_key(leftshift2,p8)
#print(key2)
print("Key1 : ", key1)
print("Key2 : ", key2)
print("Enter the plaintext")
plaintext=[]
for i in range(8):
    element=int(input())
    plaintext.append(element)
ipplaintext=permutate_key(plaintext,ip)
print("Plain text after IP")
print(ipplaintext)
extpermutate=permutate_key(ipplaintext[4:],ep)
print("After E/P Permuation")
print(extpermutate)
epxorkey1=xor_func(extpermutate,key1)
print("E/P Xor Key1 Output")
print(epxorkey1)
sboxoutput=dec_to_bin(read_s0(epxorkey1,s0))+dec_to_bin(read_s1(epxorkey1,s1))
print("SBOX output")
print(sboxoutput)
print("After p4 on SBOX Output")
pfour=permutate_key(sboxoutput,p4)
print(pfour)
pfourxorip=xor_func(ipplaintext[:4],pfour)
print("After XOR of P4 and left reserver bits")
print(pfourxorip)
print("after switching of p4 and right ip bits")
newplaintext=ipplaintext[4:]+pfourxorip
print(newplaintext)
newextpermutate=permutate_key(newplaintext[4:],ep)
print(newextpermutate)
epxorkey2=xor_func(newextpermutate,key2)
print("E/P Xor Key1 Output")
print(epxorkey2)
sboxoutput2=dec_to_bin(read_s0(epxorkey2,s0))+dec_to_bin(read_s1(epxorkey2,s1))
print("SBOX output")
print(sboxoutput2)
print("After p4 on SBOX Output2")
pfour2=permutate_key(sboxoutput2,p4)
print(pfour2)
pfourxorip2=xor_func(newplaintext[:4],pfour2)
print("After XOR of P4 and left reserver bits of new text")
print(pfourxorip2)
beforeinverse=pfourxorip2+newplaintext[4:]
print("before cipher")
print(beforeinverse)
cipher=permutate_key(beforeinverse,ipinverse)
print("Ciphertext")
print(cipher)
#----------Decrypting the Cipher-----
permutateCipher=permutate_key(cipher,ip)
eppermutateCipher=permutate_key(permutateCipher[4:],ep)
cipherxorkey2=xor_func(eppermutateCipher,key2)
ciphersboxoutput=dec_to_bin(read_s0(cipherxorkey2,s0))+dec_to_bin(read_s1(cipherxorkey2,s1))
cipherpfour=permutate_key(ciphersboxoutput,p4)
cipherpfourxorip=xor_func(permutateCipher[:4],cipherpfour)
newciphertext=permutateCipher[4:]+cipherpfourxorip
print("new cipher text")
print(newciphertext)
newcipherextpermutate=permutate_key(newciphertext[4:],ep)
cipherxorkey1=xor_func(newcipherextpermutate,key1)
#print("E/P Xor Key1 Output")
#print(epxorkey2)
ciphersboxoutput2=dec_to_bin(read_s0(cipherxorkey1,s0))+dec_to_bin(read_s1(cipherxorkey1,s1))
#print("SBOX output")
#print(sboxoutput2)
#print("After p4 on SBOX Output2")
cipherpfour2=permutate_key(ciphersboxoutput2,p4)
#print(pfour2)
cipherpfourxorip2=xor_func(newciphertext[:4],cipherpfour2)
#print("After XOR of P4 and left reserver bits of new text")
#print(pfourxorip2)
beforeplaintext=cipherpfourxorip2+newciphertext[4:]
ciphertotext=permutate_key(beforeplaintext,ipinverse)
print("Plain text")
print(ciphertotext)











