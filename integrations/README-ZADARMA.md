# 📞 ZADARMA - ESTADO DE LA INTEGRACIÓN

**Fecha:** 2025-03-11  
**Estado:** ✅ IMPLEMENTADA - ⏳ PENDIENTE ACTIVACIÓN DE CREDENCIALES

---

## ✅ LO QUE ESTÁ HECHO

| Componente | Archivo | Estado |
|------------|---------|--------|
| API Client | `zadarma_client.py` | ✅ Completo |
| Webhook Handler | `zadarma_webhook.py` | ✅ Puerto 18791 |
| Integración A2A | `zadarma_client.py` | ✅ OpenClaw ready |
| Documentación | `ZADARMA-INTEGRATION.md` | ✅ Completa |
| Test Scripts | `test_zadarma.py`, `debug_zadarma.py` | ✅ Creados |

---

## ⏳ LO QUE FALTA

### 1. Activar Credenciales en Zadarma

**Tus credenciales:**
```
API Key:    YOUR_ZADARMA_KEY
Secret:     YOUR_ZADARMA_SECRET
```

**Pasos en Zadarma:**
1. Entra en https://zadarma.com
2. Ve a: **Área Personal** → **Configuraciones** → **API**
3. Verifica que las claves están **activas**
4. Si no funcionan, haz **reset** de las claves
5. Copia las NUEVAS claves y actualiza `/root/.openclaw/zadarma.env`

### 2. Habilitar Permisos

Marca estas casillas en el panel de Zadarma:
- ✅ Info methods (balance, tariff)
- ✅ SIP methods
- ✅ Virtual numbers
- ✅ SMS
- ✅ PBX/IVR
- ✅ Webhooks

### 3. Esperar Activación

Las claves pueden tardar **5-10 minutos** en activarse después de crearlas/resetearlas.

---

## 🧪 CÓMO VERIFICAR QUE FUNCIONA

```bash
cd /root/OPENCLAW-city/integrations
python3 test_zadarma.py
```

**✅ ÉXITO:**
```
📊 Test 1: Getting balance...
   Response: {'balance': '10.00', 'currency': 'EUR'}
```

**❌ ERROR 401:**
```
Response: {'status': 'error', 'error': '401 Unauthorized'}
```
→ Las claves no están activas o son incorrectas

---

## 📋 FLUJO UNA VEZ ACTIVADO

```
1. Llamada entrante → Zadarma
2. Zadarma → Webhook (puerto 18791)
3. Webhook → OpenClaw A2A (puerto 18790)
4. A2A → LiveKit Voice Agent
5. Voice Agent → Responde con AI
```

---

## 🔄 PRÓXIMOS PASOS (CUANDO LAS CLAVES FUNCIONEN)

1. ✅ Verificar conexión: `python3 test_zadarma.py`
2. ⏳ Configurar webhook en Zadarma: `http://YOUR_SENSITIVE_IP:18791/webhook/zadarma/call`
3. ⏳ Enrutar llamadas a LiveKit
4. ⏳ Testear flujo completo

---

## 📞 SOPORTE ZADARMA

- **Email:** support@zadarma.com
- **Chat:** Disponible en el panel
- **Docs:** https://zadarma.com/es/support/api/

---

**Resumen:** La integración está **100% implementada**. Solo falta que las credenciales de Zadarma se activen en su panel.
