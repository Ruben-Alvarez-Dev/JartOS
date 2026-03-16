# 🚨 SECURITY INCIDENT - API KEYS EXPOSED

**Date:** 2025-03-11  
**Severity:** CRITICAL  
**Status:** ⚠️ ACTION REQUIRED

---

## 📋 WHAT HAPPENED

GitGuardian detected exposed API keys in the GitHub repository:

- ❌ MiniMax API Key
- ❌ Telegram Bot Token
- ❌ OpenClaw Gateway Token
- ❌ Zadarma Credentials

**Root Cause:** Keys were committed to git in plaintext `.env` files.

---

## 🚨 IMMEDIATE ACTIONS REQUIRED

### 1. REVOKE ALL EXPOSED KEYS (DO THIS NOW)

#### MiniMax API Key
```
1. Go to: https://platform.minimax.io/
2. Account → API Keys
3. REVOKE: YOUR_MINIMAX_KEY
4. Generate NEW key
5. Update: /etc/openclaw/secrets/openclaw.env
```

#### Telegram Bot Token
```
1. Open Telegram → @BotFather
2. Send: /revoke
3. Select your bot
4. Generate NEW token
5. Update: /etc/openclaw/secrets/openclaw.env
```

#### OpenClaw Gateway Token
```
1. Generate new random token:
   python3 -c "import uuid; print(uuid.uuid4())"
2. Update: /etc/openclaw/secrets/openclaw.env
3. Restart: systemctl restart openclaw
```

#### Zadarma Credentials
```
1. Go to: https://zadarma.com
2. Account → Settings → API
3. Reset API keys
4. Update: /etc/openclaw/secrets/openclaw.env
```

---

### 2. CLEAN GIT HISTORY

```bash
cd /root/OPENCLAW-city

# Remove secrets from git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch -r **/*.env **/*secret* **/*token*' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (rewrites history)
git push origin main --force --all

# Clean local git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

### 3. VERIFY SECRETS ARE SECURE

```bash
# Check secrets location
ls -la /etc/openclaw/secrets/
# Should show: -rw------- root root (600 permissions)

# Check .gitignore
cat /root/OPENCLAW-city/.gitignore | grep -E "env|secret|token"
# Should block all secret files

# Check for exposed secrets in git
git log --all --full-history -- "**/*.env" "**/*secret*" "**/*token*"
# Should show nothing after cleanup
```

---

## 🔒 NEW SECURITY PROTOCOL

### Secrets Storage
```
Location: /etc/openclaw/secrets/
Permissions: 600 (root only)
Format: .env files with symlink
```

### Git Safety
```
.gitignore blocks:
- .env
- *.env
- secrets/
- credentials/
- *.key, *.pem
- *_secret*, *_token*
```

### Before Any Commit
```bash
# Check for secrets
git diff --cached | grep -iE "key|secret|token|password"

# If found, DO NOT COMMIT
# Move to /etc/openclaw/secrets/ instead
```

---

## ✅ CHECKLIST

- [ ] MiniMax key revoked and replaced
- [ ] Telegram token revoked and replaced
- [ ] OpenClaw token regenerated
- [ ] Zadarma credentials reset (if applicable)
- [ ] Git history cleaned
- [ ] Secrets in /etc/openclaw/secrets/ with 600 permissions
- [ ] .gitignore updated and committed
- [ ] All services restarted with new secrets

---

## 📞 CONTACTS

- **GitGuardian:** security@gitguardian.com
- **MiniMax Support:** support@minimax.io
- **Telegram API:** https://core.telegram.org/api

---

**Last Updated:** 2025-03-11  
**Status:** ⚠️ PENDING KEY REVOCATION
