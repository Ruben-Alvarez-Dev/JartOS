# 📞 ZADARMA SIP TRUNK - CONFIGURACIÓN DIRECTA

**Fecha:** 2026-03-11  
**Estado:** ✅ CONFIGURADO - ⏳ PENDIENTE ACTIVAR EN ZADARMA

---

## 🎯 CONFIGURACIÓN SIMPLIFICADA

### Zadarma SIP Trunk (DIRECTO - SIN API)

```
Servidor SIP:   pbx.zadarma.com
Usuario:        553900-100
Contraseña:     qr
Extensión:      100
Display:        Supervisor
```

---

## 📋 QUÉ HACER EN ZADARMA (PASO A PASO)

### 1. Ve a tu panel de Zadarma

https://zadarma.com

### 2. Configuración de Desvío de Llamadas

```
Configuración → Desvío de llamadas → Desvío a servidor SIP
```

### 3. Activa el desvío y pon:

```
Dirección del servidor: YOUR_SENSITIVE_IP:5060
```

### 4. Guarda los cambios

### 5. ¡LISTO!

Cuando alguien llame a tu número +34919935163, la llamada llegará a tu VPS.

---

## 🔥 FIREWALL YA CONFIGURADO

```bash
# Puertos abiertos para Zadarma:
5060/udp    - SIP (185.45.152.0/24, 185.45.154.0/24, 185.45.155.0/24, etc.)
10000:20000/udp - RTP (audio)
```

---

## 🤖 MINIMAX LLM CONFIGURADO

```
Provider:     MiniMax Coding Plan
Model:        minimax-m2.5
URL:          https://api.minimax.io/v1
API Key:      YOUR_MINIMAX_KEY_PARTIAL (configurada)
```

**Ramiro ahora usa MiniMax en lugar de Mistral.**

---

## 🧪 TEST DE LLM

```bash
curl -X POST https://api.minimax.io/v1/chat/completions \
  -H "Authorization: Bearer YOUR_MINIMAX_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "minimax-m2.5",
    "messages": [{"role": "user", "content": "Hola"}]
  }'
```

---

## 📊 ESTADO ACTUAL

| Componente | Estado |
|------------|--------|
| **Zadarma SIP** | ✅ Credenciales guardadas |
| **Firewall** | ✅ Puertos abiertos |
| **LiveKit** | ✅ Escuchando puerto 5060 |
| **MiniMax LLM** | ✅ Configurado |
| **OpenClaw** | ✅ Reiniciado con nueva config |
| **Desvío Zadarma** | ⏳ PENDIENTE ACTIVAR EN PANEL |

---

## ✅ CUANDO ACTIVES EL DESVÍO EN ZADARMA

1. Llamada entra a +34919935163
2. Zadarma → SIP → Tu VPS (YOUR_SENSITIVE_IP:5060)
3. LiveKit recibe la llamada
4. Voice Agent contesta con MiniMax LLM
5. Conversación AI en tiempo real

---

**¡SOLO FALTA QUE ACTIVES EL DESVÍO EN EL PANEL DE ZADARMA!**
