#!/usr/bin/env python3
"""
Configure Zadarma SIP Forwarding via API
Trying ALL possible endpoints
"""

import hashlib
import base64
import hmac
import requests
import json

USER_KEY = "YOUR_ZADARMA_KEY"
SECRET = "YOUR_ZADARMA_SECRET"
BASE_URL = "https://api.zadarma.com/v1"

def get_signature(method, params):
    params_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    md5_params = hashlib.md5(params_str.encode()).hexdigest()
    sign_str = method + params_str + md5_params
    signature = base64.b64encode(hmac.new(SECRET.encode(), sign_str.encode(), hashlib.sha1).digest()).decode()
    return f"{USER_KEY}:{signature}"

def try_request(method, endpoint, params=None, data=None):
    """Try API request with all auth methods"""
    url = f"{BASE_URL}{endpoint}"
    
    # Method 1: Standard signature
    if params:
        auth = get_signature(method, params)
    else:
        auth = get_signature(method, {})
    
    headers = {"Authorization": auth}
    if data:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    
    try:
        if method == "GET":
            r = requests.get(url, params=params, headers=headers, timeout=10)
        elif method == "POST":
            r = requests.post(url, params=params, data=data, headers=headers, timeout=10)
        elif method == "PUT":
            r = requests.put(url, params=params, data=data, headers=headers, timeout=10)
        
        return r.status_code, r.json()
    except Exception as e:
        return 0, {"error": str(e)}

print("=== PROBANDO TODOS LOS ENDPOINTS DE ZADARMA ===\n")

# 1. Get SIP numbers
print("📋 1. GET /sip/")
code, resp = try_request("GET", "/sip/")
print(f"   {code}: {json.dumps(resp, indent=2)[:300]}\n")

# 2. Get virtual numbers
print("📋 2. GET /direct_numbers/")
code, resp = try_request("GET", "/direct_numbers/")
print(f"   {code}: {json.dumps(resp, indent=2)[:300]}\n")

# 3. Get PBX settings
print("📋 3. GET /pbx/")
code, resp = try_request("GET", "/pbx/")
print(f"   {code}: {json.dumps(resp, indent=2)[:300]}\n")

# 4. Get PBX redirection
print("📋 4. GET /pbx/redirection/")
code, resp = try_request("GET", "/pbx/redirection/", params={"pbx": "1"})
print(f"   {code}: {json.dumps(resp, indent=2)[:300]}\n")

# 5. Set SIP redirection (target endpoint!)
print("📋 5. PUT /sip/redirection/ (CONFIGURAR DESVÍO)")
data = {
    "sip": "553900-100",
    "forwarding": "YOUR_SENSITIVE_IP:5060",
    "forwarding_type": "sip",
    "forwarding_enabled": "1"
}
code, resp = try_request("PUT", "/sip/redirection/", data=data)
print(f"   {code}: {json.dumps(resp, indent=2)[:300]}\n")

# 6. Alternative: Set via PBX
print("📋 6. POST /pbx/redirection/ (ALTERNATIVA)")
data = {
    "pbx": "1",
    "forwarding": "YOUR_SENSITIVE_IP:5060",
    "forwarding_enabled": "1"
}
code, resp = try_request("POST", "/pbx/redirection/", data=data)
print(f"   {code}: {json.dumps(resp, indent=2)[:300]}\n")

# 7. Get account info
print("📋 7. GET /info/")
code, resp = try_request("GET", "/info/")
print(f"   {code}: {json.dumps(resp, indent=2)[:300]}\n")

# 8. Check if keys work at all
print("📋 8. GET /info/balance/ (VERIFICAR CREDENCIALES)")
code, resp = try_request("GET", "/info/balance/")
print(f"   {code}: {json.dumps(resp, indent=2)[:300]}\n")

print("\n=== CONCLUSIÓN ===")
print("Si TODOS dan 401: Las credenciales NO están activas en Zadarma")
print("Si ALGUNO funciona: Usar ese endpoint para configurar")
print("\nContacta con Zadarma soporte: support@zadarma.com")
print(f"Keys: {USER_KEY} / {SECRET}")
