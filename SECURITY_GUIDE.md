# 🔐 Security Guide - Protecting API Keys & Secrets

**Project**: JobMetrics Pro
**Last Updated**: 2025-10-28
**Priority**: 🔴 CRITICAL - Read before pushing to GitHub!

---

## 🚨 URGENT: Before Pushing to GitHub

### ⚠️ STOP! Have you checked these?

- [ ] `.env` file is in `.gitignore` (and NOT staged for commit)
- [ ] No API keys in any Python files
- [ ] No API keys in any markdown documentation
- [ ] Pre-commit hook is working
- [ ] You're using `.env.example` for public sharing

**If you're not sure, read this entire guide first!**

---

## 🎯 Quick Start: Secure Setup (5 minutes)

### 1. Verify .env is Protected

```bash
# Check if .env is in .gitignore
grep "^.env$" .gitignore

# Output should show: .env
```

### 2. Test Pre-commit Hook

```bash
# The hook should be executable
ls -la .git/hooks/pre-commit

# Should show: -rwxr-xr-x (the 'x' means executable)
```

### 3. Verify .env is NOT Staged

```bash
# Check git status
git status

# .env should NOT appear in "Changes to be committed"
# If it does, run: git reset HEAD .env
```

### 4. Use .env.example for Sharing

```bash
# This file is SAFE to commit (no real keys)
cat .env.example

# Should show placeholder: ANTHROPIC_API_KEY=sk-ant-api03-YOUR_API_KEY_HERE
```

---

## 🛡️ Multi-Layer Security System

We've implemented **5 layers of protection**:

### Layer 1: .gitignore 🚫
**What**: Tells git to ignore sensitive files
**Files Protected**:
- `.env` (your secrets)
- `.env.local`
- `.env.*.local`
- `*.key`, `*.pem` (certificates)
- `secrets/` folder

**Test**:
```bash
git check-ignore .env
# Should output: .env (means it's ignored)
```

---

### Layer 2: .env.example ✅
**What**: Public template with NO real secrets
**Purpose**: Show others what environment variables they need
**Safe to commit**: YES ✅

**What's inside**:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_API_KEY_HERE
```

**How to use**:
```bash
# New user clones your repo and runs:
cp .env.example .env

# Then they fill in their own API keys in .env
```

---

### Layer 3: Pre-commit Hook 🔍
**What**: Automatically scans for secrets before EVERY commit
**Location**: `.git/hooks/pre-commit`

**What it detects**:
- Anthropic API keys (sk-ant-api03-...)
- Generic API key patterns
- Passwords in code
- Secret tokens
- .env file accidentally staged
- Certificate files (.key, .pem)

**How it works**:
```bash
# When you try to commit
git add somefile.py
git commit -m "Update code"

# Hook runs automatically:
🔍 Scanning for secrets before commit...
✓ No secrets detected. Commit proceeding...
```

**If secrets found**:
```bash
⚠️  SECURITY WARNING: Potential secret found in config.py
⛔ COMMIT BLOCKED: Potential secrets detected!
```

**To test the hook**:
```bash
# Try to stage .env (should be blocked)
git add .env
git commit -m "test"

# Should show: ⛔ BLOCKED: .env file is staged for commit!
```

---

### Layer 4: Runtime Environment Variables 🔐
**What**: Load secrets from .env at runtime (never hardcode)
**How**: Use `python-dotenv` library

**Good ✅**:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file
api_key = os.getenv('ANTHROPIC_API_KEY')
```

**Bad ❌**:
```python
# NEVER do this!
api_key = "sk-ant-api03-lCr0Bf609ETdBYnsy1CUB3goRPfb..."
```

---

### Layer 5: GitHub Secrets (for CI/CD) 🤖
**What**: Store secrets securely on GitHub for automated workflows
**When to use**: GitHub Actions, automated deployment

**Setup**:
1. Go to: GitHub Repo → Settings → Secrets and variables → Actions
2. Click: "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: `sk-ant-api03-...` (your real key)
5. Click: "Add secret"

**Use in GitHub Actions**:
```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    steps:
      - name: Deploy with API key
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: ./deploy.sh
```

---

## 🔥 Emergency: I Accidentally Committed My API Key!

### Step 1: Rotate Your API Key IMMEDIATELY ⚡
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Revoke the exposed API key
3. Generate a new one
4. Update your `.env` file with new key

**Why**: Anyone can see GitHub history, even after you delete the file!

---

### Step 2: Remove from Git History

**Option A: Recent commit (easy)**
```bash
# If it was your last commit
git reset --soft HEAD~1   # Undo commit (keeps changes)
git reset HEAD .env       # Unstage .env
# Fix the file, then commit again
```

**Option B: Remove from all history (advanced)**
```bash
# Use BFG Repo-Cleaner (recommended)
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Remove file from all commits
bfg --delete-files .env

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (WARNING: rewrites history)
git push --force
```

**Option C: Use git filter-branch**
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

git push --force
```

⚠️ **WARNING**: Options B & C rewrite git history. Coordinate with your team!

---

### Step 3: Verify Removal
```bash
# Search entire git history for the API key
git log -S "sk-ant-api03" --all

# Should return nothing
```

---

## 📋 Pre-Push Checklist

Before `git push` to GitHub, verify:

### Security Checklist
- [ ] `.env` is in `.gitignore`
- [ ] `.env` is NOT in `git status`
- [ ] Pre-commit hook is working (`ls -la .git/hooks/pre-commit`)
- [ ] `.env.example` has ONLY placeholders (no real keys)
- [ ] No API keys in Python files (`grep -r "sk-ant-api03" src/`)
- [ ] No API keys in markdown docs (`grep -r "sk-ant-api03" *.md`)

### Test Commands
```bash
# 1. Check .env is ignored
git check-ignore .env
# Expected: .env

# 2. Check what's staged
git status
# Expected: .env should NOT appear

# 3. Search for API keys in code
grep -r "sk-ant-api03" src/ docs/ *.py *.md
# Expected: No output (or only .env.example with placeholder)

# 4. Test pre-commit hook
echo "sk-ant-api03-test" > test_secret.txt
git add test_secret.txt
git commit -m "test"
# Expected: ⚠️  SECURITY WARNING (hook blocks it)
rm test_secret.txt
git reset HEAD test_secret.txt
```

---

## 🎓 Best Practices

### 1. Never Hardcode Secrets
❌ **Bad**:
```python
API_KEY = "sk-ant-api03-lCr0Bf609ETdBYnsy1CUB3goRPfb..."
client = anthropic.Anthropic(api_key=API_KEY)
```

✅ **Good**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=API_KEY)
```

---

### 2. Use Environment-Specific Files
```bash
.env.local          # Your local secrets (ignored)
.env.example        # Public template (committed)
.env.production     # Production secrets (ignored)
```

---

### 3. Validate Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found! "
        "Copy .env.example to .env and add your API key."
    )
```

---

### 4. Document Required Variables
In `README.md`:
```markdown
## Setup

1. Copy environment template:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

2. Get your API key from [Anthropic Console](https://console.anthropic.com/)

3. Add to `.env`:
   \`\`\`
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   \`\`\`
```

---

### 5. Rotate Keys Regularly
- **Monthly**: Rotate API keys (even if not exposed)
- **Immediately**: Rotate if suspicious activity detected
- **Always**: Rotate after team member leaves

---

## 🔍 How to Check for Leaked Secrets

### GitHub Secret Scanning
GitHub automatically scans for leaked secrets in public repos:
- Go to: Repo → Security → Secret scanning alerts
- Fix any alerts immediately!

### Manual Search
```bash
# Search for API keys in all files
grep -r "sk-ant-api03" .

# Search git history
git log -S "sk-ant-api03" --all --oneline

# Check what's being committed
git diff --cached | grep -i "api"
```

### Third-Party Tools
- [GitGuardian](https://www.gitguardian.com/) - Scan repos for secrets
- [TruffleHog](https://github.com/trufflesecurity/trufflehog) - Find secrets in git history
- [git-secrets](https://github.com/awslabs/git-secrets) - Prevent committing secrets

---

## 📚 Additional Resources

### Official Documentation
- [Anthropic API Keys](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

### Security Tools
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [GitGuardian](https://www.gitguardian.com/)
- [TruffleHog](https://github.com/trufflesecurity/trufflehog)

### Security Best Practices
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [12-Factor App: Config](https://12factor.net/config)

---

## ❓ FAQ

### Q: Is .env.example safe to commit?
**A**: YES! It only contains placeholders like `YOUR_API_KEY_HERE`, not real secrets.

### Q: Can I skip the pre-commit hook?
**A**: Technically yes (`git commit --no-verify`), but **DON'T DO IT**. The hook protects you from mistakes.

### Q: What if I need to share my API key with a teammate?
**A**: Use a secure password manager (1Password, LastPass) or your team's secret management system. NEVER send via Slack, email, or commit to git.

### Q: I pushed a secret months ago. Is it still dangerous?
**A**: YES! Git history is permanent. Anyone can clone your repo and see old commits. Rotate the key and remove from history.

### Q: How do I know if my API key is exposed?
**A**:
1. Check GitHub Security → Secret scanning alerts
2. Monitor API usage in Anthropic Console for unusual activity
3. Use GitGuardian to scan your repo

---

## ✅ Summary

**3 Things to Remember**:
1. **NEVER** commit `.env` (it's in `.gitignore`)
2. **ALWAYS** use `.env.example` for sharing templates
3. **IMMEDIATELY** rotate keys if exposed

**You're protected by**:
- ✅ .gitignore blocks .env
- ✅ Pre-commit hook scans for secrets
- ✅ .env.example for safe sharing
- ✅ Runtime environment variables
- ✅ GitHub Secrets for CI/CD

**If something goes wrong**:
1. Rotate API key immediately
2. Remove from git history
3. Verify removal with `git log -S`

---

**Stay secure! 🔐**

*Last updated: 2025-10-28 by Jerry Lai*
