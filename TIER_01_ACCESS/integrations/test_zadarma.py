#!/usr/bin/env python3
"""
Test Zadarma API Connection
"""

import sys
sys.path.insert(0, '/root/OPENCLAW-city/integrations')

from zadarma_client import ZadarmaClient

# Load credentials
with open('/root/.openclaw/zadarma.env') as f:
    creds = {}
    for line in f:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            creds[key] = value

print("=== TEST ZADARMA API ===\n")
print(f"User Key: {creds.get('ZADARMA_USER_KEY', 'N/A')[:10]}...")
print(f"Secret: {'*' * 10}")
print()

# Initialize client
zadarma = ZadarmaClient(
    user_key=creds.get('ZADARMA_USER_KEY'),
    secret=creds.get('ZADARMA_SECRET')
)

# Test 1: Get balance
print("📊 Test 1: Getting balance...")
balance = zadarma.get_balance()
print(f"   Response: {balance}")
print()

# Test 2: Get tariff
print("💰 Test 2: Getting tariff...")
tariff = zadarma.get_tariff()
print(f"   Response: {tariff}")
print()

# Test 3: Get SIP numbers
print("📞 Test 3: Getting SIP numbers...")
sip_numbers = zadarma.get_sip_numbers()
print(f"   Response: {sip_numbers}")
print()

# Test 4: Get virtual numbers
print("🔢 Test 4: Getting virtual numbers...")
virtual_numbers = zadarma.get_virtual_numbers()
print(f"   Response: {virtual_numbers}")
print()

# Test 5: Get timezone
print("🌍 Test 5: Getting timezone...")
timezone = zadarma.get_timezone()
print(f"   Response: {timezone}")
print()

print("=== TEST COMPLETE ===")
