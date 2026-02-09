# Netlify Setup Guide - know.crpg.info

## ✅ Completed Steps

### 1. Netlify API Token Secured
- **Location:** `C:\Users\mova\obsidian\OneNoteExport\16-Creds\03-Infrastructure\netlify-api-token.md`
- **Token:** `nfp_hCPiKGsMkoaKhm7MS1VxAvfHsFV8KsLga343`
- **Status:** ✅ Stored securely outside repository

### 2. Netlify Configuration Created
- **File:** `netlify.toml`
- **Build Command:** `npx quartz build`
- **Publish Directory:** `public`
- **Node Version:** 22
- **Status:** ✅ Committed to repository

### 3. Git Remote Connected
- **Repository:** https://github.com/movanet/know-crpg-tenur
- **Branch:** main
- **Commit:** f1f4133 - Initial commit with 275 files
- **Status:** ✅ Pushed successfully

### 4. Files Committed and Pushed
- **Framework Files:** 275 files, 37,263 insertions
- **Content Pages:** 92 water tenure knowledge base pages
- **Status:** ✅ All files on GitHub

## 🔄 Next Steps: Connect Netlify

You have two options to connect Netlify. **Option A (Web UI) is recommended** for first-time setup.

### Option A: Netlify Web UI (Recommended)

1. **Visit Netlify Dashboard**
   ```
   https://app.netlify.com
   ```

2. **Import from GitHub**
   - Click "Add new site" → "Import an existing project"
   - Choose "Deploy with GitHub"
   - Authorize Netlify to access GitHub (if not already authorized)

3. **Select Repository**
   - Search for: `movanet/know-crpg-tenur`
   - Click on the repository

4. **Verify Build Settings**
   - Netlify should auto-detect from `netlify.toml`:
     - **Build command:** `npx quartz build`
     - **Publish directory:** `public`
     - **Node version:** 22
   - If not detected, enter these manually

5. **Deploy Site**
   - Click "Deploy site"
   - Wait for initial build (~2-3 minutes)
   - Build log will show real-time progress

6. **Configure Custom Domain**
   - After deployment, go to "Site settings" → "Domain management"
   - Click "Add custom domain"
   - Enter: `know.crpg.info`
   - Follow DNS configuration instructions (see DNS section below)

7. **Enable HTTPS**
   - Netlify automatically provisions Let's Encrypt SSL
   - Wait for SSL certificate (usually 5-10 minutes after DNS propagation)

### Option B: Netlify CLI (Alternative)

If you prefer command-line setup:

```bash
cd "C:\Users\mova\obsidian\OneNoteExport\01-Projects\07-CimanukFAO\know-crpg-tenur"

# Install Netlify CLI globally (if not installed)
npm install -g netlify-cli

# Login with API token
netlify login --auth nfp_hCPiKGsMkoaKhm7MS1VxAvfHsFV8KsLga343

# Initialize and link to new site
netlify init

# Follow prompts:
# - Create & configure a new site
# - Choose team
# - Site name: know-crpg-tenur (or your preferred name)
# - Build command: npx quartz build
# - Publish directory: public
```

This creates `.netlify/state.json` (already in `.gitignore`).

## 🌐 DNS Configuration

After creating the Netlify site, you need to configure DNS for `know.crpg.info`.

### Find Your Domain Registrar

First, check where `crpg.info` domain is registered:

```bash
# Check domain registrar
whois crpg.info | findstr "Registrar"
```

Or visit: https://lookup.icann.org/en/lookup

### DNS Records Required

**Option 1: CNAME Record (Recommended)**
```
Type    Name               Value
CNAME   know.crpg.info     <site-name>.netlify.app
```

**Option 2: A + AAAA Records (Alternative)**
```
Type    Name               Value
A       know.crpg.info     75.2.60.5
AAAA    know.crpg.info     2a05:d014:edb:5400::9
```

### Where to Add DNS Records

Common registrars:
- **Cloudflare:** DNS → Add Record
- **Namecheap:** Advanced DNS → Add New Record
- **GoDaddy:** DNS Management → Add Record
- **Route53:** Hosted Zones → Create Record

**DNS Propagation Time:** 5-60 minutes (check at https://dnschecker.org)

## 🚀 Verify Auto-Deploy Works

Once Netlify is connected, test the auto-deploy feature:

### 1. Make a Small Content Change

```bash
cd "C:\Users\mova\obsidian\OneNoteExport\01-Projects\07-CimanukFAO\know-crpg-tenur"

# Edit the index page
notepad content\index.md

# Add a line like: "Last updated: [today's date]"
```

### 2. Commit and Push

```bash
git add .
git commit -m "Test auto-deploy: Update index page"
git push
```

### 3. Watch Deployment

- Visit: https://app.netlify.com/sites/<site-name>/deploys
- You should see a new deployment triggered automatically
- Build time: ~14 seconds
- Total deployment time: ~30 seconds

### 4. Verify Changes Live

- Visit: https://know.crpg.info (or your Netlify URL)
- Refresh the page
- Your changes should appear within 30-60 seconds

## 📊 Build Information

**Expected Build Output:**
```
✓ Emitted 353 files to public/ in 13.94s
✓ Build completed successfully
```

**Build Stats:**
- Pages: 92 content pages
- Generated files: 353 files
- Build time: ~14 seconds
- Content language: Bahasa Indonesia
- Framework: Quartz v4.5.2

## 🔐 Security Checklist

- ✅ API token stored outside repository
- ✅ `.env` excluded in `.gitignore`
- ✅ `.netlify/` excluded in `.gitignore`
- ✅ `node_modules` excluded
- ✅ `public/` excluded (build artifacts)
- ⚠️ Never commit API tokens to git

## 🎯 Success Criteria

Your deployment is successful when:

- ✅ GitHub repository shows all 275 files
- ✅ Netlify site created and connected to GitHub
- ✅ Initial deployment completed successfully
- ✅ Site accessible at Netlify URL (`<site-name>.netlify.app`)
- ✅ Custom domain `know.crpg.info` configured
- ✅ SSL certificate provisioned and active
- ✅ Auto-deploy triggered by git push
- ✅ All 92 content pages rendering correctly

## 📝 Useful Commands

### Check Repository Status
```bash
cd "C:\Users\mova\obsidian\OneNoteExport\01-Projects\07-CimanukFAO\know-crpg-tenur"
git status
git log --oneline -5
```

### View Remote Configuration
```bash
git remote -v
```

### Build Locally (Testing)
```bash
npx quartz build
# Output: public/ directory with 353 files
```

### Check Netlify Site Status (CLI)
```bash
netlify status
netlify open
```

## 🆘 Troubleshooting

### Build Fails on Netlify

**Check build logs:** https://app.netlify.com/sites/<site-name>/deploys

**Common issues:**
- Node version mismatch → Verify `netlify.toml` has `NODE_VERSION = "22"`
- Missing dependencies → Check `package.json` and `package-lock.json` are committed
- Build command error → Test locally: `npx quartz build`

### Domain Doesn't Resolve

**Check DNS propagation:** https://dnschecker.org/?domain=know.crpg.info

**Verify DNS records:**
- Check registrar DNS settings
- Ensure records point to correct Netlify target
- Wait 5-60 minutes for propagation

### SSL Certificate Not Provisioning

**Requirements:**
- DNS must be fully propagated
- Domain must resolve to Netlify servers
- Usually takes 5-10 minutes after DNS propagation

**Force renewal:** Site settings → Domain management → HTTPS → Renew certificate

### Auto-Deploy Not Triggering

**Check webhook:**
- GitHub repo → Settings → Webhooks
- Should show Netlify webhook with recent deliveries
- Click webhook to see delivery history

**Verify Netlify settings:**
- Site settings → Build & deploy → Continuous deployment
- Should show "Deploy on push" enabled

## 📚 Additional Resources

- **Netlify Dashboard:** https://app.netlify.com
- **GitHub Repository:** https://github.com/movanet/know-crpg-tenur
- **Quartz Documentation:** https://quartz.jzhao.xyz
- **DNS Checker:** https://dnschecker.org
- **SSL Labs Test:** https://www.ssllabs.com/ssltest/

## 🔄 Future Workflow

Once setup is complete, your workflow will be:

1. **Edit content locally** in `content/` folder
2. **Commit changes:** `git add . && git commit -m "Description"`
3. **Push to GitHub:** `git push`
4. **Automatic deployment** (30-60 seconds)
5. **Verify on live site:** https://know.crpg.info

---

**Project:** FAO Cimanuk - Water Tenure Assessment
**Framework:** Quartz v4.5.2
**Content:** 92 pages (Bahasa Indonesia)
**Domain:** know.crpg.info
**Setup Date:** 2026-02-09
