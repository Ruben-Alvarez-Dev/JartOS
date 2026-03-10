# 🤝 Contributing to OpenClaw-city

**Guía de Contribución**

Gracias por tu interés en contribuir a OpenClaw-city. Esta guía te ayudará a empezar.

---

## 📋 Índice

1. [Código de Conducta](#código-de-conducta)
2. [Cómo Contribuir](#cómo-contribuir)
3. [Reportar Bugs](#reportar-bugs)
4. [Solicitar Features](#solicitar-features)
5. [Pull Requests](#pull-requests)
6. [Estándares de Código](#estándares-de-código)

---

## Código de Conducta

Este proyecto sigue un [Código de Conducta](CODE_OF_CONDUCT.md). Por favor, léelo antes de participar.

---

## Cómo Contribuir

### Tipos de Contribución

- 🐛 **Reportar bugs** - Issues de errores
- 💡 **Solicitar features** - Nuevas funcionalidades
- 📝 **Documentación** - Mejorar docs
- 🔧 **Código** - Fixes y features
- 🧪 **Testing** - Tests y QA
- 💬 **Discusión** - Feedback y ideas

### Flujo de Contribución

1. **Fork** el repositorio
2. **Crea una rama** para tu feature/fix
3. **Desarrolla** tus cambios
4. **Testea** tus cambios
5. **Commit** con mensajes claros
6. **Push** a tu fork
7. **Pull Request** al repositorio principal

---

## Reportar Bugs

### Antes de Reportar

- [ ] Verificar que el bug no está ya reportado
- [ ] Probar con la última versión
- [ ] Revisar la documentación

### Template de Bug Report

```markdown
**Descripción:**
Descripción clara y concisa del bug.

**Para Reproducir:**
Pasos para reproducir:
1. Configurar '...'
2. Ejecutar '...'
3. Ver error '...'

**Comportamiento Esperado:**
Qué debería pasar.

**Comportamiento Actual:**
Qué pasa actualmente.

**Screenshots:**
Si aplica, añadir screenshots.

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- OpenClaw version: [e.g. 2026.3.10]
- Python version: [e.g. 3.10]

**Logs:**
```
Pegar logs relevantes aquí
```

**Información Adicional:**
Cualquier otro contexto relevante.
```

---

## Solicitar Features

### Antes de Solicitar

- [ ] Verificar que el feature no está ya solicitado
- [ ] Revisar si existe workaround
- [ ] Considerar si es útil para otros usuarios

### Template de Feature Request

```markdown
**Descripción:**
Descripción clara del feature solicitado.

**Problema a Resolver:**
Qué problema resuelve este feature.

**Solución Propuesta:**
Cómo debería funcionar el feature.

**Alternativas Consideradas:**
Otras soluciones que has considerado.

**Contexto Adicional:**
Cualquier otro contexto relevante.
```

---

## Pull Requests

### Antes de Enviar un PR

- [ ] Tu código sigue los estándares del proyecto
- [ ] Has testeado tus cambios
- [ ] Has actualizado la documentación si es necesario
- [ ] Los tests existentes pasan (si aplica)

### Proceso de Review

1. **Envía tu PR** con descripción clara
2. **Mantenedores revisan** el código
3. **Feedback** si hay cambios necesarios
4. **Aprobación** y merge

### Template de PR

```markdown
**Descripción:**
Descripción clara de los cambios.

**Tipo de Cambio:**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**Issue Relacionado:**
Fixes #123 (si aplica)

**Testing:**
Cómo has testeado los cambios.

**Checklist:**
- [ ] Código sigue estándares
- [ ] Tests pasan
- [ ] Documentación actualizada
- [ ] Sin breaking changes no documentados
```

---

## Estándares de Código

### Python

```python
# Usar type hints
def calculate_score(value: float, threshold: float = 0.5) -> bool:
    """Calcular score basado en threshold.
    
    Args:
        value: Valor a evaluar
        threshold: Threshold de corte
        
    Returns:
        True si value >= threshold, False otherwise
    """
    return value >= threshold

# Usar docstrings
# Seguir PEP 8
```

### Bash

```bash
#!/bin/bash
# Usar set -e para errores
set -e

# Usar variables en mayúsculas
CONFIG_FILE="/etc/config.json"

# Usar funciones para código reusable
check_service() {
    local service=$1
    systemctl is-active "$service"
}
```

### Documentación

```markdown
# Usar headers claros
## Subsecciones

# Usar código con syntax highlighting
```python
print("Hello")
```

# Usar listas y tablas cuando aplique
```

---

## Desarrollo Local

### Setup

```bash
# Fork y clonar
git clone https://github.com/tu-usuario/OPENCLAW-city.git
cd OPENCLAW-city

# Crear rama
git checkout -b feature/my-feature

# Desarrollar cambios
# ...

# Commit
git commit -m "feat: add my feature"

# Push
git push origin feature/my-feature
```

### Convención de Commits

```
feat: nueva funcionalidad
fix: corrección de bug
docs: actualización de documentación
style: cambios de formato (sin cambio de lógica)
refactor: refactorización de código
test: añadir/modificar tests
chore: cambios de configuración/build
```

---

## Preguntas Frecuentes

### ¿Cuánto tarda un PR en ser revieweado?

Generalmente 1-7 días dependiendo de la complejidad.

### ¿Puedo ayudar sin saber programar?

¡Sí! La documentación, testing y reportes de bugs son muy valiosos.

### ¿Necesito firmar un CLA?

No, no requerimos Contributor License Agreement.

---

## Contacto

- **GitHub Issues:** Para bugs y features
- **Discussions:** Para preguntas generales
- **Email:** security@openclaw.ai (para seguridad)

---

¡Gracias por contribuir a OpenClaw-city! 🦞
