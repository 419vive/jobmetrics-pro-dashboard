# 🔐 Security Quick Reference Card

**⏱️ 2-Minute Version** of [SECURITY_GUIDE.md](SECURITY_GUIDE.md)

---

## ✅ Before Your First Push to GitHub

```bash
# 1. Verify .env is protected
git check-ignore .env
# Should output: .env

# 2. Test the pre-commit hook works
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x (executable)

# 3. Verify .env is NOT staged
git status
# .env should NOT appear in "Changes to be committed"
```

---

## 🛡️ What Protects Your API Keys

| Layer | What | Status |
|-------|------|--------|
| 1 | `.gitignore` blocks .env | ✅ Active |
| 2 | `.env.example` for sharing | ✅ Created |
| 3 | Pre-commit hook scans secrets | ✅ Installed |
| 4 | Load from environment at runtime | ✅ Using python-dotenv |
| 5 | GitHub Secrets for CI/CD | 📋 Use when needed |

---

## 🚨 If You Accidentally Commit a Secret

### 1️⃣ Rotate the API key IMMEDIATELY
Go to [Anthropic Console](https://console.anthropic.com/) → Revoke old key → Generate new

### 2️⃣ Remove from git history
```bash
# If it was your last commit
git reset --soft HEAD~1
git reset HEAD .env
# Fix, then commit again

# If it's in older commits
# Use BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/
```

### 3️⃣ Verify removal
```bash
git log -S "sk-ant-api03" --all
# Should return nothing
```

---

## ✅ Pre-Push Checklist

- [ ] `.env` in `.gitignore`? → `grep "^.env$" .gitignore`
- [ ] `.env` not staged? → `git status`
- [ ] Pre-commit hook working? → Try committing test secret
- [ ] No secrets in code? → `grep -r "sk-ant-api03" src/`

---

## 📚 Files You Created

| File | Safe to Commit? | Purpose |
|------|-----------------|---------|
| `.env` | ❌ NO | Your real API keys (ignored by git) |
| `.env.example` | ✅ YES | Template with placeholders |
| `.git/hooks/pre-commit` | Auto-created | Scans for secrets |
| `SECURITY_GUIDE.md` | ✅ YES | Full security documentation |

---

## 💡 Common Commands

```bash
# Setup for new user
cp .env.example .env
# Then edit .env with real API key

# Check what's ignored
git status --ignored

# Test pre-commit hook manually
.git/hooks/pre-commit

# Search for secrets in code
grep -r "sk-ant-api03" . --exclude-dir=.git
```

---

## ❓ Quick FAQ

**Q: Can I commit .env.example?**
A: YES! It only has placeholders.

**Q: What if pre-commit hook blocks me?**
A: Remove the secret from your code. DON'T use `--no-verify`.

**Q: How to share API key with teammate?**
A: Use password manager. NEVER via Slack/email/git.

---

**🔒 Remember**: `.env` = SECRET (never commit) | `.env.example` = PUBLIC (safe to share)

For full details, see **[SECURITY_GUIDE.md](SECURITY_GUIDE.md)**
