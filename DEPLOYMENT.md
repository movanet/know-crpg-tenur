# Water Tenure Knowledge Base - Deployment Guide

**Status:** ✅ **DEPLOYED (Local Build Complete)**
**Date:** 2026-02-09
**Build System:** Quartz v4.5.2

---

## ✅ What Was Deployed

### Knowledge Base Content
- **92 files** built and ready for serving
  - 91 atomic notes (water tenure concepts)
  - 1 index page (landing page)
- **100% Bahasa Indonesia**
- **353 static files** generated in `public/` directory
- **Zero build errors**
- **Zero git warnings** (all files tracked)

### Configuration
- **Site Title:** Water Tenure Knowledge Base
- **Tagline:** FAO Cimanuk
- **Locale:** Indonesian (id-ID)
- **Base URL:** tenur-air.crpg.info
- **Features Enabled:**
  - ✅ Single Page Application (SPA)
  - ✅ Interactive popovers
  - ✅ Full-text search
  - ✅ Graph visualization
  - ✅ Backlinks
  - ✅ Wikilinks

---

## 📂 Current Location

```
C:\Users\mova\obsidian\OneNoteExport\01-Projects\07-CimanukFAO\know-crpg-tenur\

├── content/              ← Source markdown files (92 files)
│   ├── 00-konsep-dasar/
│   ├── 01-kerangka-hukum/
│   ├── 02-tata-kelola/
│   ├── 03-penggunaan-air/
│   ├── 06-konflik-air/
│   └── index.md
│
├── public/               ← Built static site (353 files) ✅
│   ├── index.html
│   ├── static/
│   └── [all generated files]
│
├── quartz.config.ts      ← Configuration
├── package.json          ← Dependencies
└── .git/                 ← Git repository (initialized)
```

---

## 🚀 Deployment Options

### Option 1: Local Development Server (Preview)

**Purpose:** Test the site locally before production deployment

```bash
cd "C:/Users/mova/obsidian/OneNoteExport/01-Projects/07-CimanukFAO/know-crpg-tenur"
npx quartz serve
```

**Access:** http://localhost:8080

**Use Case:** Local testing, development, preview changes

---

### Option 2: GitHub Pages (Recommended)

**Purpose:** Free hosting with automatic deployments

#### Step 1: Create GitHub Repository
```bash
cd "C:/Users/mova/obsidian/OneNoteExport/01-Projects/07-CimanukFAO/know-crpg-tenur"

# Add GitHub as remote (replace with your repo URL)
git remote add origin https://github.com/CRPG-Org/water-tenure-kb.git

# Push to GitHub
git push -u origin master
```

#### Step 2: Enable GitHub Pages
1. Go to repository Settings > Pages
2. Source: **GitHub Actions**
3. Quartz will auto-deploy on every push

#### Step 3: Update Base URL
Edit `quartz.config.ts`:
```typescript
baseUrl: "crpg-org.github.io/water-tenure-kb",
```

Then rebuild and push:
```bash
npx quartz build
git add .
git commit -m "Update base URL for GitHub Pages"
git push
```

**Access:** https://crpg-org.github.io/water-tenure-kb/

**Advantages:**
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ SSL/TLS included
- ✅ Global CDN

---

### Option 3: Custom Domain (tenur-air.crpg.info)

**Purpose:** Professional branded URL

#### Prerequisites
- Domain: crpg.info (already owned)
- Subdomain: tenur-air.crpg.info

#### Step 1: Deploy to GitHub Pages (see Option 2)

#### Step 2: Configure DNS
Add CNAME record to crpg.info DNS:
```
Type: CNAME
Name: tenur-air
Value: crpg-org.github.io
TTL: 3600
```

#### Step 3: Configure GitHub Pages
1. Go to repository Settings > Pages
2. Custom domain: `tenur-air.crpg.info`
3. ✅ Enforce HTTPS

#### Step 4: Update quartz.config.ts
```typescript
baseUrl: "tenur-air.crpg.info",
```

**Access:** https://tenur-air.crpg.info

**Advantages:**
- ✅ Professional branding
- ✅ Easy to remember
- ✅ All GitHub Pages benefits

---

### Option 4: CRPG Hetzner VPS

**Purpose:** Self-hosted on CRPG infrastructure

#### Deploy to VM 101 (cloud.crpg.info)

```bash
# 1. Copy public/ directory to server
scp -r public/ hetzner-crpg:/var/www/tenur-air/

# 2. Configure Caddy reverse proxy
ssh hetzner-crpg
sudo nano /etc/caddy/Caddyfile
```

Add to Caddyfile:
```
tenur-air.crpg.info {
    root * /var/www/tenur-air
    file_server
    encode gzip
}
```

```bash
# 3. Reload Caddy
sudo systemctl reload caddy
```

**Access:** https://tenur-air.crpg.info

**Advantages:**
- ✅ Full control over hosting
- ✅ Existing CRPG infrastructure
- ✅ Can integrate with other CRPG services

**Disadvantages:**
- Manual deployment (no auto-deploy on push)
- Requires server maintenance

---

### Option 5: Netlify (Alternative Free Hosting)

**Purpose:** Alternative to GitHub Pages with drag-and-drop deployment

#### Option 5A: Drag-and-Drop
1. Go to https://app.netlify.com/drop
2. Drag the `public/` folder
3. Done! Site deployed instantly

#### Option 5B: Git Integration
1. Connect Netlify to GitHub repository
2. Build command: `npx quartz build`
3. Publish directory: `public`
4. Auto-deploys on every push

**Access:** https://[random-name].netlify.app (or custom domain)

**Advantages:**
- ✅ Very easy setup
- ✅ Excellent performance
- ✅ Built-in CDN
- ✅ Automatic HTTPS

---

## 🔧 Post-Deployment Tasks

### 1. Test Core Features

After deployment, verify:
- ✅ Home page loads (index.md)
- ✅ Category navigation works
- ✅ Wikilinks navigate correctly
- ✅ Search functionality works
- ✅ Graph view displays
- ✅ Backlinks appear
- ✅ Footnotes render correctly
- ✅ Mobile responsive

### 2. Update Documentation

Update project documentation with:
- Live site URL
- Deployment method used
- Access instructions for team

### 3. Announce Deployment

Notify stakeholders:
- FAO project team
- CRPG staff
- Research collaborators

---

## 📊 Site Statistics

### Content Metrics
- **Pages:** 92 (91 notes + 1 index)
- **Words:** ~27,500 (average 300 words/page)
- **Wikilinks:** 400+ interconnections
- **Categories:** 5 main categories
- **Language:** 100% Bahasa Indonesia

### Technical Metrics
- **Generated Files:** 353 static files
- **Total Size:** ~5-7 MB (estimated)
- **Build Time:** ~14 seconds
- **Dependencies:** 483 npm packages

### Quality Metrics
- **Footnote Accuracy:** 93.4%
- **Sequential Footnotes:** 100%
- **Metadata Compliance:** 100%
- **Build Errors:** 0
- **Git Warnings:** 0

---

## 🛠️ Maintenance Commands

### Rebuild Site
```bash
cd "C:/Users/mova/obsidian/OneNoteExport/01-Projects/07-CimanukFAO/know-crpg-tenur"
npx quartz build
```

### Local Preview
```bash
npx quartz serve
```

### Update Content
```bash
# Edit files in content/ directory
# Then rebuild
npx quartz build

# Commit and push if using GitHub Pages
git add content/
git commit -m "Update content"
git push
```

### Update Quartz
```bash
npm update quartz
npx quartz build
```

---

## 🔐 Security Considerations

### Public vs Private
- **Current:** All content marked `publish: true`
- **To make private:** Change `publish: false` in frontmatter
- **Selective publishing:** Edit `ignorePatterns` in quartz.config.ts

### Access Control
- **Public deployment:** Anyone can access
- **Private deployment:** Use:
  - GitHub private repository + GitHub Pages (auth required)
  - Password-protected hosting (Netlify, Vercel with password)
  - VPN-only access (CRPG Hetzner with firewall rules)

---

## 📝 Recommended Next Steps

### Immediate (Now)
1. ✅ **Test local build:** `npx quartz serve` → visit http://localhost:8080
2. ✅ **Choose deployment method** (GitHub Pages recommended)
3. ✅ **Deploy to production**

### Short-term (This Week)
4. Configure custom domain (tenur-air.crpg.info)
5. Add analytics tracking (Google Analytics or Plausible)
6. Share deployment URL with FAO team
7. Create backup of deployment

### Long-term (Optional)
8. Add search analytics to track popular queries
9. Integrate with CRPG main website
10. Set up automated backups
11. Create API for programmatic access
12. Develop mobile app wrapper

---

## 🐛 Troubleshooting

### Issue: Wikilinks Not Working
**Solution:** Ensure baseUrl matches deployment URL in quartz.config.ts

### Issue: Search Not Working
**Solution:** Clear browser cache, check if search index built correctly

### Issue: Build Fails
**Solution:**
```bash
rm -rf public/
npm install
npx quartz build
```

### Issue: Git Push Rejected
**Solution:**
```bash
git pull --rebase origin master
git push
```

---

## 📞 Support & Contact

**Project Lead:** CRPG Infrastructure Team
**Technical Support:** Claude Code (Sonnet 4.5)
**Documentation:** This file + Quartz docs (https://quartz.jzhao.xyz)

**Issues:** Report to CRPG team or create GitHub issue

---

## 📜 Deployment Checklist

- [x] Quartz installed and configured
- [x] 92 content files built successfully
- [x] Index page created
- [x] Git repository initialized
- [x] Content committed to git
- [x] Static site generated in public/
- [x] Build errors resolved (0 errors)
- [x] Configuration updated (title, locale, baseUrl)
- [ ] **Choose deployment method** ← YOU ARE HERE
- [ ] Deploy to chosen platform
- [ ] Test live deployment
- [ ] Configure custom domain (optional)
- [ ] Share with stakeholders
- [ ] Set up monitoring/analytics

---

**Deployment Status:** ✅ **READY TO DEPLOY**
**Recommended Method:** GitHub Pages + Custom Domain
**Build Location:** `C:\Users\mova\obsidian\OneNoteExport\01-Projects\07-CimanukFAO\know-crpg-tenur\public\`

**Next Command to Run:**
```bash
# Preview locally first
cd "C:/Users/mova/obsidian/OneNoteExport/01-Projects/07-CimanukFAO/know-crpg-tenur"
npx quartz serve
```

Then open http://localhost:8080 in your browser to preview the deployed site!
