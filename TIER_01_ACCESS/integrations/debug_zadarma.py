#!/usr/bin/env python3
"""Debug Zadarma signature"""

import hashlib
import base64
import hmac
import requests

USER_KEY = "YOUR_ZADARMA_KEY"
SECRET = "YOUR_ZADARMA_SECRET"

method = "/info/balance/"
params = {}

# Build signature
sorted_params = sorted(params.items())
params_list = [f"{k}={v}" for k, v in sorted_params]
params_str = "&".join(params_list)

print(f"Method: {method}")
print(f"Params: {params}")
print(f"Params str: '{params_str}'")

md5_params = hashlib.md5(params_str.encode()).hexdigest()
print(f"MD5 params: {md5_params}")

sign_str = method + params_str + md5_params
print(f"Sign str: {sign_str}")

signature = base64.b64encode(
    hmac.new(SECRET.encode(), sign_str.encode(), hashlib.sha1).digest()
).decode()

print(f"Signature: {signature}")

auth_header = f"{USER_KEY}:{signature}"
print(f"Auth header: {auth_header}")

# Make request
url = f"https://api.zadarma.com/v1{method}"
headers = {"Authorization": auth_header}

print(f"\nRequest URL: {url}")
print(f"Headers: {headers}")

response = requests.get(url, headers=headers, timeout=10)
print(f"\nResponse status: {response.status_code}")
print(f"Response body: {response.text}")
