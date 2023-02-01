import optparse
from socket import *

def connScan(tgtHost, tgtPort):
    try:
        # TODO Create socket
        s = socket()
        # TODO Connect to target host and port
        s.connect((tgtHost, tgtPort))
        print('[+]%d/tcp open'% tgtPort) 
        # TODO Send garbage data (any string you want)
        s.send("Hello".encode('utf-8'))
        # TODO Get results from sending garbage string
        results = s.recv(1024).decode('utf-8')
        print('[+] ' + str(results))
        # TODO close the socket
        s.close()
    except:
        print('[-]%d/tcp closed'% tgtPort)

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host" %tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: ' + tgtName[0])
    except:
        print('\n[+] Scan Results for: ' + tgtIP)
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        print('Scanning port ' + tgtPort)
        # TODO thread the scan so that you run connScan for each target on a separate thread.
        connScan(tgtHost, int(tgtPort))

def main():
    parser = optparse.OptionParser("usage%prog "+ "-H <target host> -p <target port>")
    parser.add_option('-H', dest='tgtHost', type='string',  help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string',  help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(', ')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print('[-] You must specify a target host and port[s].')
        exit(0)
    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()
