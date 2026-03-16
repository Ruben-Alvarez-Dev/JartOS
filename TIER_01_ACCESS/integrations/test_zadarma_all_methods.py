#!/usr/bin/env python3
"""Test Zadarma with different auth approaches"""

import hashlib
import base64
import hmac
import requests

USER_KEY = "YOUR_ZADARMA_KEY"
SECRET = "YOUR_ZADARMA_SECRET"

print("=== PROBANDO DIFERENTES MÉTODOS DE AUTENTICACIÓN ===\n")

# Method 1: Standard HMAC-SHA1 (Zadarma docs)
print("📋 Método 1: HMAC-SHA1 estándar (docs Zadarma)")
method = "/info/balance/"
params = {}
params_str = ""
md5_params = hashlib.md5(params_str.encode()).hexdigest()
sign_str = method + params_str + md5_params
signature = base64.b64encode(hmac.new(SECRET.encode(), sign_str.encode(), hashlib.sha1).digest()).decode()
auth1 = f"{USER_KEY}:{signature}"
print(f"   Sign string: {sign_str}")
print(f"   Signature: {signature}")
print(f"   Auth: {auth1}")

r1 = requests.get("https://api.zadarma.com/v1/info/balance/", 
                  headers={"Authorization": auth1}, timeout=10)
print(f"   Result: {r1.status_code} - {r1.text[:100]}")
print()

# Method 2: Simple API key in header
print("📋 Método 2: API Key directa en header")
r2 = requests.get("https://api.zadarma.com/v1/info/balance/",
                  headers={"Authorization": f"Bearer {USER_KEY}"}, timeout=10)
print(f"   Result: {r2.status_code} - {r2.text[:100]}")
print()

# Method 3: API Key + Secret en header separado
print("📋 Método 3: Key y Secret separados")
r3 = requests.get("https://api.zadarma.com/v1/info/balance/",
                  headers={
                      "X-API-Key": USER_KEY,
                      "X-API-Secret": SECRET
                  }, timeout=10)
print(f"   Result: {r3.status_code} - {r3.text[:100]}")
print()

# Method 4: Parámetros en URL
print("📋 Método 4: Parámetros en URL")
r4 = requests.get(f"https://api.zadarma.com/v1/info/balance/?api_key={USER_KEY}", timeout=10)
print(f"   Result: {r4.status_code} - {r4.text[:100]}")
print()

# Method 5: Verificar si las keys son válidas (longitud)
print("📋 Método 5: Verificación de formato")
print(f"   Key length: {len(USER_KEY)} chars")
print(f"   Secret length: {len(SECRET)} chars")
print(f"   Key format: {'✅ Alphanumeric' if USER_KEY.isalnum() else '❌ Invalid'}")
print(f"   Secret format: {'✅ Alphanumeric' if SECRET.isalnum() else '❌ Invalid'}")
print()

# Method 6: Contactar soporte
print("📋 Método 6: Verificación de API")
r6 = requests.get("https://api.zadarma.com/", timeout=10)
print(f"   API Root: {r6.status_code}")
print()

print("=== CONCLUSIÓN ===")
print("Si todos los métodos fallan con 401, las credenciales NO están activas en Zadarma.")
print("Contacta con support@zadarma.com con tus claves:")
print(f"   API Key: {USER_KEY}")
print(f"   Secret: {SECRET}")
