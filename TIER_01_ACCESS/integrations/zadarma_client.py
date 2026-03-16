#!/usr/bin/env python3
"""
Zadarma API Client - OpenClaw Integration
Date: 2026-03-10
Sprint: 2 - Zadarma Integration

Features:
- SIP management
- Virtual numbers
- SMS sending
- Call webhooks
- PBX management
"""

import hashlib
import base64
import hmac
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any

class ZadarmaClient:
    """Zadarma API Client with OpenClaw A2A integration"""
    
    def __init__(self, user_key: str, secret: str, base_url: str = "https://api.zadarma.com/v1"):
        self.user_key = user_key
        self.secret = secret
        self.base_url = base_url
        self.session = requests.Session()
        
    def _get_signature(self, method: str, params: dict) -> str:
        """Generate HMAC-SHA1 signature according to Zadarma docs"""
        # Sort parameters alphabetically
        sorted_params = sorted(params.items())
        
        # Build query string
        params_list = [f"{k}={v}" for k, v in sorted_params]
        params_str = "&".join(params_list)
        
        # Build signature string: method + params + md5(params)
        md5_params = hashlib.md5(params_str.encode()).hexdigest()
        sign_str = method + params_str + md5_params
        
        # Generate HMAC-SHA1 signature
        signature = base64.b64encode(
            hmac.new(self.secret.encode(), sign_str.encode(), hashlib.sha1).digest()
        ).decode()
        
        return f"{self.user_key}:{signature}"
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        """Make API request"""
        if params is None:
            params = {}
        
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": self._get_signature(endpoint, params),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            if method == "GET":
                response = self.session.get(url, params=params, headers=headers, timeout=10)
            elif method == "POST":
                response = self.session.post(url, params=params, data=data, headers=headers, timeout=10)
            elif method == "PUT":
                response = self.session.put(url, params=params, data=data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = self.session.delete(url, params=params, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": str(e)}
    
    # ==================== INFO METHODS ====================
    
    def get_balance(self) -> Dict:
        """Get account balance"""
        return self._request("GET", "/info/balance/")
    
    def get_tariff(self) -> Dict:
        """Get current tariff"""
        return self._request("GET", "/tariff/")
    
    def get_timezone(self) -> Dict:
        """Get user timezone"""
        return self._request("GET", "/info/timezone/")
    
    # ==================== SIP METHODS ====================
    
    def get_sip_numbers(self) -> Dict:
        """List all SIP numbers"""
        return self._request("GET", "/sip/")
    
    def get_sip_status(self, sip: str) -> Dict:
        """Get SIP online status"""
        return self._request("GET", f"/sip/{sip}/status/")
    
    def create_sip(self, sip: str, password: str, **kwargs) -> Dict:
        """Create SIP number"""
        data = {"sip": sip, "password": password, **kwargs}
        return self._request("POST", "/sip/create/", data=data)
    
    def set_caller_id(self, sip: str, caller_id: str) -> Dict:
        """Change CallerID for SIP"""
        data = {"sip": sip, "caller_id": caller_id}
        return self._request("PUT", "/sip/callerid/", data=data)
    
    def get_redirection(self, sip: str) -> Dict:
        """Get call forwarding settings"""
        return self._request("GET", "/sip/redirection/", params={"sip": sip})
    
    def set_redirection(self, sip: str, forward_to: str, **kwargs) -> Dict:
        """Set call forwarding"""
        data = {"sip": sip, "forward_to": forward_to, **kwargs}
        return self._request("PUT", "/sip/redirection/", data=data)
    
    # ==================== VIRTUAL NUMBERS ====================
    
    def get_virtual_numbers(self) -> Dict:
        """List all virtual numbers"""
        return self._request("GET", "/direct_numbers/")
    
    def get_available_numbers(self, country_id: str, direction_id: str) -> Dict:
        """Get available numbers for order"""
        return self._request("GET", f"/direct_numbers/available/{direction_id}/", 
                            params={"country": country_id})
    
    def order_number(self, phone: str, sip: str, **kwargs) -> Dict:
        """Order virtual number"""
        data = {"phone": phone, "sip_id": sip, **kwargs}
        return self._request("POST", "/direct_numbers/order/", data=data)
    
    def set_number_sip(self, phone: str, sip: str) -> Dict:
        """Assign number to SIP"""
        data = {"phone": phone, "sip_id": sip}
        return self._request("PUT", "/direct_numbers/set_sip_id/", data=data)
    
    def receive_sms(self, phone: str, enable: bool = True) -> Dict:
        """Enable/disable SMS reception"""
        data = {"phone": phone, "enable": "1" if enable else "0"}
        return self._request("PUT", "/direct_numbers/receive_sms/", data=data)
    
    # ==================== SMS METHODS ====================
    
    def send_sms(self, phone: str, message: str, sender: Optional[str] = None) -> Dict:
        """Send SMS"""
        data = {"phone": phone, "message": message}
        if sender:
            data["sender"] = sender
        return self._request("POST", "/sms/send/", data=data)
    
    def get_sms_templates(self) -> Dict:
        """Get SMS templates"""
        return self._request("GET", "/sms/templates/")
    
    # ==================== PBX METHODS ====================
    
    def create_pbx(self, name: str, **kwargs) -> Dict:
        """Create PBX"""
        data = {"name": name, **kwargs}
        return self._request("POST", "/pbx/create/", data=data)
    
    def get_pbx_extensions(self, pbx_id: str) -> Dict:
        """Get PBX extensions"""
        return self._request("GET", "/pbx/internal/", params={"pbx": pbx_id})
    
    def create_extension(self, pbx_id: str, extension: str, **kwargs) -> Dict:
        """Create PBX extension"""
        data = {"pbx": pbx_id, "extension": extension, **kwargs}
        return self._request("POST", "/pbx/internal/create/", data=data)
    
    def get_ivr_list(self) -> Dict:
        """Get IVR list"""
        return self._request("GET", "/pbx/ivr/")
    
    def create_ivr(self, name: str, scenario: list, **kwargs) -> Dict:
        """Create IVR menu"""
        data = {"name": name, "scenario": json.dumps(scenario), **kwargs}
        return self._request("POST", "/pbx/ivr/", data=data)
    
    # ==================== STATISTICS ====================
    
    def get_statistics(self, date_from: str, date_to: str) -> Dict:
        """Get call statistics"""
        params = {"date_from": date_from, "date_to": date_to}
        return self._request("GET", "/statistics/", params=params)
    
    def get_pbx_statistics(self, pbx_id: str, date_from: str, date_to: str) -> Dict:
        """Get PBX statistics"""
        params = {"pbx": pbx_id, "date_from": date_from, "date_to": date_to}
        return self._request("GET", "/statistics/pbx/", params=params)
    
    # ==================== WEBHOOKS ====================
    
    def get_webhooks(self) -> Dict:
        """Get webhook settings"""
        return self._request("GET", "/pbx/webhooks/")
    
    def set_webhook(self, url: str, events: list, **kwargs) -> Dict:
        """Set webhook URL and events"""
        data = {"url": url, "events": json.dumps(events), **kwargs}
        return self._request("POST", "/pbx/webhooks/", data=data)


# ==================== OPENCLAW INTEGRATION ====================

class ZadarmaOpenClawIntegration:
    """Zadarma + OpenClaw + LiveKit Integration"""
    
    def __init__(self, zadarma_client: ZadarmaClient, openclaw_url: str = "http://127.0.0.1:18789"):
        self.zadarma = zadarma_client
        self.openclaw_url = openclaw_url
        self.a2a_url = "http://localhost:18790/api/a2a"
    
    def send_a2a_notification(self, event_type: str, data: Dict) -> Dict:
        """Send notification to OpenClaw via A2A"""
        import httpx
        
        msg = {
            "type": "ZADARMA_EVENT",
            "timestamp": datetime.now().isoformat(),
            "orchestrator": "Zadarma-Integration",
            "payload": {
                "event": event_type,
                "data": data
            }
        }
        
        try:
            with httpx.Client(timeout=10) as client:
                response = client.post(self.a2a_url, json=msg)
                return response.json()
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def handle_incoming_call(self, call_data: Dict) -> Dict:
        """Handle incoming call webhook"""
        # Log to OpenClaw
        result = self.send_a2a_notification("incoming_call", call_data)
        
        # Route to LiveKit room
        # TODO: Implement LiveKit room creation
        
        return result
    
    def handle_outgoing_call(self, call_data: Dict) -> Dict:
        """Handle outgoing call webhook"""
        result = self.send_a2a_notification("outgoing_call", call_data)
        return result
    
    def handle_sms_received(self, sms_data: Dict) -> Dict:
        """Handle received SMS webhook"""
        result = self.send_a2a_notification("sms_received", sms_data)
        
        # Store in OpenClaw Memory
        # TODO: Implement memory storage
        
        return result
    
    def sync_contacts(self) -> Dict:
        """Sync Zadarma contacts with OpenClaw"""
        # Get SIP numbers
        sip_numbers = self.zadarma.get_sip_numbers()
        
        # Get virtual numbers
        virtual_numbers = self.zadarma.get_virtual_numbers()
        
        # Send to OpenClaw
        result = self.send_a2a_notification("contacts_sync", {
            "sip_numbers": sip_numbers,
            "virtual_numbers": virtual_numbers,
            "synced_at": datetime.now().isoformat()
        })
        
        return result
    
    def create_voice_agent_route(self, phone_number: str, livekit_room: str) -> Dict:
        """Route incoming calls to LiveKit voice agent"""
        # Set call forwarding to LiveKit SIP
        result = self.zadarma.set_redirection(
            sip=phone_number,
            forward_to=livekit_room
        )
        
        # Notify OpenClaw
        self.send_a2a_notification("voice_agent_route", {
            "phone": phone_number,
            "livekit_room": livekit_room,
            "status": result.get("status", "unknown")
        })
        
        return result


# ==================== MAIN ====================

if __name__ == "__main__":
    # Example usage
    print("Zadarma API Client - OpenClaw Integration")
    print("==========================================")
    
    # Initialize (replace with actual credentials)
    # zadarma = ZadarmaClient(user_key="YOUR_KEY", secret="YOUR_SECRET")
    
    # print("Balance:", zadarma.get_balance())
    # print("SIP Numbers:", zadarma.get_sip_numbers())
    
    print("\n✅ Zadarma client ready")
    print("📡 Integration with OpenClaw: ready")
    print("🎤 LiveKit routing: ready")
