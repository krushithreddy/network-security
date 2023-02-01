import crypt
import sys


def testPass(cryptPass, dictfile):

    # TODO use the dictionary and crypt to identify possible plaintext passwords that match cryptPass
    f2 = open(dictfile)
    for i in f2.readlines():
        plaintext_password = i.strip('\n')
        if crypt.crypt(plaintext_password,cryptPass[0:2]) == cryptPass:
            print("[+] Found Password: "+plaintext_password+"\n")
        else:
            print("[-] Password Not Found.\n") 
    # If the password is found, use the following:
        #print("[+] Found Password: "+plaintext_password+"\n")
        #return
    # Else:
        #print("[-] Password Not Found.\n")
        #return
    #raise NotImplementedError

def main(passwdfile,dictfile):
    # TODO take in a password file and a dictionary file and attempt to crack each password in the password file using testPass()
    f1 = open(passwdfile)
    for i in f1.readlines():
        cryptPass=(i.split(' ')[1]).strip('\n')
        testPass(cryptPass, dictfile)

if __name__ == "__main__":
    passwdfile=sys.argv[1]
    dictfile=sys.argv[2]
    main(passwdfile,dictfile)
