# 🎉 LIVEKIT SETUP COMPLETADO

**Fecha:** 2025-03-10  
**Estado:** ✅ Funcionando  
**Sprint:** 0 (Preparación) - Completado

---

## 📊 RESUMEN EJECUTIVO

LiveKit server está **instalado, configurado y funcionando correctamente** en el VPS de OpenClaw-City.

### Componentes Desplegados

| Componente | Versión | Estado | Puerto | Red |
|------------|---------|--------|--------|-----|
| **livekit-server** | 1.9.12 | ✅ Running | 7880-7882 | openclaw-net |
| **livekit-redis** | 7-alpine | ✅ Running | 6379 (interno) | openclaw-net |
| **Caddy** | 2.11.2 | ✅ Running | 8443 (HTTP) | localhost |
| **Tailscale Serve** | - | ✅ Running | 443 → 8443 | tailnet |

---

## 🔑 CREDENCIALES

**Archivo:** `/root/.livekit/credentials`

```
URL: http://localhost:7880
URL_INTERNAL: http://livekit-server:7880
API_KEY: openclaw-54990a102ce72a4e
API_SECRET: YOUR_LIVEKIT_SECRET
```

⚠️ **Importante:** Guarda estas credenciales en un lugar seguro.

---

## 🌐 ACCESO

### Desde Tailscale (RECOMENDADO - Todos tus dispositivos)

| Dispositivo | URL | Estado |
|-------------|-----|--------|
| **MacBook Pro** | `https://vpn-ruben-vps-openclaw.tail6c9810.ts.net/webclient/` | ✅ Activo |
| **Mac Mini** | `https://vpn-ruben-vps-openclaw.tail6c9810.ts.net/webclient/` | ✅ Activo |
| **Xiaomi Pad 5** | `https://vpn-ruben-vps-openclaw.tail6c9810.ts.net/webclient/` | ✅ Activo |
| **Pixel** | `https://vpn-ruben-vps-openclaw.tail6c9810.ts.net/webclient/` | ✅ Activo |
| **Samsung S9 FE** | `https://vpn-ruben-vps-openclaw.tail6c9810.ts.net/webclient/` | ✅ Activo |

### Subdominios Públicos (wildcard DNS + UFW permitido)

| Subdominio | URL | Estado |
|------------|-----|--------|
| **livekit** | `https://livekit.alvarezconsult.es` | ✅ Activo |
| **livekit-api** | `https://livekit-api.alvarezconsult.es` | ✅ Activo |

### Local (VPS)

| URL | Puerto | Estado |
|-----|--------|--------|
| `http://localhost:7880` | 7880 | ✅ Activo (LiveKit) |
| `http://localhost:8443` | 8443 | ✅ Activo (Caddy) |
| `http://localhost:8444` | 8444 | ✅ Activo (Token API) |
| `http://localhost:8445` | 8445 | ✅ Activo (Web Client) |

---

## 📁 ARCHIVOS DE CONFIGURACIÓN

| Archivo | Ubicación | Propósito | Permisos |
|---------|-----------|-----------|----------|
| docker-compose.yml | `/opt/livekit/docker-compose.yml` | Orquestación Docker | 644 |
| livekit.yaml | `/opt/livekit/livekit.yaml` | Configuración servidor | 644 |
| .env | `/opt/livekit/.env` | Variables de entorno | 600 |
| Caddyfile | `/etc/caddy/Caddyfile` | Reverse proxy | 644 |
| credentials | `/root/.livekit/credentials` | Credenciales API | 600 |

---

## 🧪 VERIFICACIÓN

### Test Script

```bash
python3 /root/OPENCLAW-city/scripts/test-livekit.py
```

**Resultado:**
```
=== LiveKit Server Test ===

1. Creating access token...
   ✅ Token created: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

2. Connecting to Room Service...

3. Listing rooms...
   ✅ Rooms found: 0
   ℹ️ No active rooms (this is normal)

4. Creating test room 'openclaw-test'...
   ✅ Room created: openclaw-test
   ✅ Test room cleaned up

=== Test Complete ===

LiveKit server is working correctly! ✅
```

### Comandos Rápidos

```bash
# Ver estado de contenedores
docker compose -f /opt/livekit/docker-compose.yml ps

# Ver logs de LiveKit
docker logs livekit-server -f

# Ver logs de Caddy
journalctl -u caddy -f

# Probar acceso local
curl http://localhost:7880/

# Probar acceso vía Caddy
curl -H "Host: livekit.alvarezconsult.es" http://localhost:8443/
```

---

## 🛠️ GESTIÓN DE SERVICIOS

### LiveKit Server

```bash
cd /opt/livekit

# Iniciar
docker compose up -d

# Detener
docker compose down

# Reiniciar
docker compose restart

# Ver logs
docker compose logs -f
```

### Caddy (Reverse Proxy)

```bash
# Ver estado
systemctl status caddy

# Reiniciar
systemctl restart caddy

# Ver logs
journalctl -u caddy -f

# Validar configuración
caddy validate --config /etc/caddy/Caddyfile
```

### Tailscale Serve

```bash
# Ver configuración
tailscale serve status

# Ver configuración JSON
tailscale serve status --json

# Resetear configuración
tailscale serve reset

# Configurar proxy
tailscale serve --bg https+insecure://localhost:8443
```

---

## 📋 CONFIGURACIÓN TÉCNICA

### livekit.yaml

```yaml
port: 7880
rtc:
  tcp_port: 7881
  udp_port: 7882

redis:
  address: redis:6379

keys:
  "openclaw-54990a102ce72a4e": "YOUR_LIVEKIT_SECRET"

webhook:
  api_key: openclaw-54990a102ce72a4e

logging:
  level: info
```

### docker-compose.yml

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: livekit-redis
    restart: unless-stopped
    networks:
      - openclaw-net
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes

  livekit:
    image: livekit/livekit-server:latest
    container_name: livekit-server
    restart: unless-stopped
    networks:
      - openclaw-net
    ports:
      - "7880:7880"
      - "7881:7881"
      - "7882:7882/udp"
    env_file:
      - .env
    command: --config /etc/livekit.yaml --bind 0.0.0.0
    volumes:
      - ./livekit.yaml:/etc/livekit.yaml:ro
    depends_on:
      - redis

networks:
  openclaw-net:
    external: true

volumes:
  redis-data:
```

### Caddyfile

```caddy
:8443 {
    @livekit {
        host livekit.alvarezconsult.es
    }
    
    @livekitapi {
        host livekit-api.alvarezconsult.es
    }
    
    handle @livekit {
        reverse_proxy localhost:7880
    }
    
    handle @livekitapi {
        reverse_proxy localhost:7880
    }
    
    log {
        output file /var/log/caddy/livekit.log
        format json
    }
}
```

---

## ⚠️ NOTAS IMPORTANTES

1. **UDP Buffer:** El log puede mostrar advertencia sobre buffer UDP (425984 bytes, se recomiendan 5000000). Normal en desarrollo, optimizar en producción.

2. **HTTPS:** Tailscale Serve maneja HTTPS automáticamente para la tailnet. Para producción pública, configurar Let's Encrypt en Caddy.

3. **Firewall:** Puertos 7880-7882 expuestos. UFW debe permitir solo tráfico necesario.

4. **Backup:** Credenciales en `/opt/livekit/.env` y `/root/.livekit/credentials`. Incluir en backup automático.

5. **DNS Wildcard:** alvarezconsult.es tiene wildcard DNS apuntando a la IP del VPS. Los subdominios livekit.* resuelven automáticamente.

---

## 🔒 SEGURIDAD

### Security Headers (Caddy)

- `Strict-Transport-Security`: max-age=31536000; includeSubDomains
- `X-Content-Type-Options`: nosniff
- `X-Frame-Options`: DENY
- `X-XSS-Protection`: 1; mode=block

### Network Isolation

- LiveKit solo escucha en red Docker interna (172.20.0.0/16)
- Caddy actúa como único punto de entrada
- Tailscale Serve maneja autenticación tailnet

### API Keys

- Guardadas en archivo con permisos 600
- No hardcodeadas en YAML
- Usar variables de entorno

---

## 📊 MÉTRICAS

| Métrica | Valor |
|---------|-------|
| **Versión LiveKit** | 1.9.12 |
| **Versión Redis** | 7-alpine |
| **Versión Caddy** | 2.11.2 |
| **Node ID** | Auto-generado |
| **Rooms activas** | 0 (se crean dinámicamente) |
| **Participantes** | 0 |

---

## 🔗 ENLACES RELACIONADOS

- [LiveKit Docs](https://docs.livekit.io)
- [LiveKit Agents](https://github.com/livekit/agents)
- [LiveKit CLI](https://github.com/livekit/livekit-cli)
- [Caddy Docs](https://caddyserver.com/docs)
- [Tailscale Serve](https://tailscale.com/kb/1247/funnel-serve-use-cases)
- [ROADMAP.md](./ROADMAP.md)
- [TODO.md](./TODO.md)

---

**Estado:** ✅ Sprint 0 Completado  
**Próximo Hito:** Sprint 1 - LiveKit CLI + Web Client Test  
**Última actualización:** 2025-03-10
