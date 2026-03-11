# 🔑 CONFIGURACIÓN DE CREDENCIALES ZADARMA

## 📍 DÓNDE ENCONTRAR LAS API KEYS

1. **Inicia sesión** en tu panel de Zadarma: https://zadarma.com
2. Ve a: **Configuración** → **Claves y API** (o **API Settings**)
3. **Genera nuevas claves** si no existen
4. **Copia** las dos claves:
   - **API Key** (user_key)
   - **Secret Key** (secret)

---

## ⚠️ FORMATO DE LAS CLAVES

Las claves de Zadarma suelen tener este formato:

- **API Key**: 20-40 caracteres alfanuméricos (ej: `a1b2c3d4e5f6g7h8i9j0...`)
- **Secret Key**: 20-40 caracteres alfanuméricos

**Las claves que me diste:**
```
Key:    YOUR_ZADARMA_KEY (20 chars) ⚠️ Parece corta
Secret: YOUR_ZADARMA_SECRET (20 chars) ⚠️ Parece corta
```

**Posibles problemas:**
1. ❌ Claves incompletas (copiaste solo parte)
2. ❌ Claves de un entorno de prueba/sandbox
3. ❌ Claves no activadas (esperan confirmación)
4. ❌ Claves sin permisos para los endpoints

---

## 🔧 CONFIGURAR CREDENCIALES

### 1. Editar archivo de configuración

```bash
nano /root/.openclaw/zadarma.env
```

### 2. Añadir las claves COMPLETAS

```env
ZADARMA_USER_KEY=tu_api_key_completa_aqui
ZADARMA_SECRET=tu_secret_completo_aqui
ZADARMA_WEBHOOK_URL=http://YOUR_SENSITIVE_IP:18791
```

### 3. Guardar y proteger

```bash
chmod 600 /root/.openclaw/zadarma.env
```

---

## ✅ VERIFICAR CREDENCIALES

Ejecuta el script de test:

```bash
cd /root/OPENCLAW-city/integrations
python3 test_zadarma.py
```

**Resultado esperado:**
```
📊 Test 1: Getting balance...
   Response: {'balance': '10.00', 'currency': 'EUR'}

💰 Test 2: Getting tariff...
   Response: {'tariff': '...', ...}
```

**Si ves error 401:**
- Las claves son incorrectas o están incompletas
- Las claves no están activadas
- Las claves no tienen permisos

---

## 📋 PERMISOS NECESARIOS

En el panel de Zadarma, asegúrate de que las claves tienen permisos para:

- ✅ **Info methods** (balance, tariff, timezone)
- ✅ **SIP methods** (list, create, redirection)
- ✅ **Virtual numbers** (order, set_sip_id)
- ✅ **SMS** (send, templates)
- ✅ **PBX** (create, extensions, IVR)
- ✅ **Webhooks** (notify events)

---

## 🔗 ENLACES ÚTILES

- **Panel Zadarma:** https://zadarma.com
- **API Docs:** https://zadarma.com/en/support/api/
- **GitHub:** https://github.com/Zadarma
- **Soporte:** support@zadarma.com

---

## 🆘 SOLUCIÓN DE PROBLEMAS

| Problema | Solución |
|----------|----------|
| Error 401 Unauthorized | Verifica que las claves están completas y activas |
| Error 403 Forbidden | Las claves no tienen permisos para ese endpoint |
| Error 429 Too Many Requests | Has superado el límite (100 req/min) |
| Error de conexión | Verifica que tienes acceso a internet |

---

**Una vez tengas las claves correctas, ejecuta:**
```bash
python3 test_zadarma.py
```
