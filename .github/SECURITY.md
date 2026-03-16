# 🔐 Security Policy

**Política de Seguridad de OpenClaw-city**

---

## 📋 Índice

1. [Reportar Vulnerabilidades](#reportar-vulnerabilidades)
2. [Proceso de Divulgación](#proceso-de-divulgación)
3. [Vulnerabilidades Conocidas](#vulnerabilidades-conocidas)
4. [Mejores Prácticas de Seguridad](#mejores-prácticas-de-seguridad)

---

## Reportar Vulnerabilidades

### Canales de Reporte

| Tipo | Canal | Tiempo de Respuesta |
|------|-------|---------------------|
| **Vulnerabilidad Crítica** | security@openclaw.ai | < 24 horas |
| **Vulnerabilidad No Crítica** | GitHub Security Advisories | < 7 días |
| **Preocupación de Seguridad** | GitHub Issues | < 7 días |

### Qué Incluir en el Reporte

```markdown
**Tipo de Vulnerabilidad:**
[e.g. XSS, SQL Injection, Auth Bypass]

**Descripción:**
Descripción clara de la vulnerabilidad.

**Impacto:**
Qué puede hacer un atacante si explota esta vulnerabilidad.

**Pasos para Reproducir:**
1. ...
2. ...
3. ...

**Prueba de Concepto:**
Código o pasos para demostrar la vulnerabilidad.

**Recomendación de Fix:**
Cómo sugerirías arreglar la vulnerabilidad.

**Información de Contacto:**
Tu email o método de contacto preferido.
```

### Qué NO Hacer

- ❌ No reportar vulnerabilidades en issues públicos
- ❌ No explotar vulnerabilidades más allá de lo necesario para demostrar
- ❌ No acceder a datos de otros usuarios
- ❌ No causar daño al sistema

---

## Proceso de Divulgación

### Timeline

```
Día 0: Reporte recibido
       ↓
Día 1: Confirmación de recepción
       ↓
Día 1-7: Análisis y validación
       ↓
Día 7-30: Desarrollo de fix
       ↓
Día 30-60: Testing del fix
       ↓
Día 60-90: Divulgación pública
```

### Responsabilidades

**Reportante:**
- Proporcionar detalles claros
- Mantener confidencialidad hasta divulgación
- Cooperar en validación del fix

**Mantenedores:**
- Responder en tiempo adecuado
- Desarrollar y testear fix
- Divulgar públicamente después de fix
- Dar crédito al reportante (si desea)

---

## Vulnerabilidades Conocidas

### Histórico

| CVE | Fecha | Severidad | Estado | Descripción |
|-----|-------|-----------|--------|-------------|
| N/A | - | - | - | Sin vulnerabilidades conocidas |

### Programa de Bug Bounty

Actualmente **no tenemos** programa de bug bounty monetario.

**Reconocimiento:**
- ✅ Crédito en CHANGELOG
- ✅ Mención en SECURITY.md
- ✅ Hall of Fame (opcional)

---

## Mejores Prácticas de Seguridad

### Para Usuarios

#### Configuración Segura

```bash
# 1. Gateway en loopback
"gateway": { "bind": "loopback" }

# 2. Autenticación activada
"gateway": { "auth": { "mode": "token" } }

# 3. Tools restringidos
"tools": { "profile": "messaging" }

# 4. Permisos correctos
chmod 600 /home/openclaw/.openclaw/.env
```

#### Rotación de Credenciales

```bash
# Rotar token de gateway mensualmente
sudo openclaw-token gateway token "$(uuidgen)"

# Rotar API keys si hay sospecha de compromiso
```

#### Monitoreo

```bash
# Verificar security score diariamente
openclaw-dashboard <<< "status"

# Revisar logs de seguridad semanalmente
openclaw-dashboard <<< "security 100"

# Ejecutar auditoría mensual
openclaw security audit --deep
```

### Para Desarrolladores

#### Código Seguro

```python
# ✅ Usar parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ❌ No usar string concatenation
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ Validar input
if not re.match(r'^[a-zA-Z0-9_]+$', username):
    raise ValueError("Invalid username")

# ✅ Usar HTTPS para APIs externas
requests.post("https://api.example.com", ...)

# ❌ No hardcodear secrets
api_key = os.environ.get("API_KEY")  # ✅
api_key = "sk-123456"  # ❌
```

#### Manejo de Secrets

```bash
# ✅ Usar variables de entorno
export API_KEY="secret"

# ✅ Usar archivos con permisos restringidos
chmod 600 .env

# ❌ No commitear secrets
echo ".env" >> .gitignore
```

---

## Configuración de Seguridad del Repositorio

### GitHub Security Features

- ✅ **Security Advisories:** Habilitado
- ✅ **Dependabot:** Habilitado para actualizaciones
- ✅ **Code Scanning:** Deshabilitado (repo privado)
- ✅ **Secret Scanning:** Habilitado

### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## Contacto de Seguridad

| Rol | Contacto |
|-----|----------|
| **Security Team** | security@openclaw.ai |
| **Lead Maintainer** | GitHub @Ruben-Alvarez-Dev |

---

## Reconocimientos

Gracias a los siguientes reportantes por ayudar a mantener OpenClaw-city seguro:

| Nombre | Vulnerabilidad | Fecha |
|--------|----------------|-------|
| (Tu nombre aquí) | - | - |

---

**Última actualización:** 2025-03-10
