# Deployment Guide

This guide explains how to deploy ApiFlow's landing page and demos to GitHub Pages.

## Quick Start

Your site will automatically deploy when you push to the `main` branch.

**Live URLs:**
- Landing page: `https://YOUR_USERNAME.github.io/apiflow/`
- Demo index: `https://YOUR_USERNAME.github.io/apiflow/demo-index.html`
- Demos: `https://YOUR_USERNAME.github.io/apiflow/demos/dark-pro/`

---

## Initial Setup

### 1. Enable GitHub Pages

1. Go to your GitHub repository settings
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select:
   - **Source:** GitHub Actions
4. Click **Save**

### 2. Commit and Push

```bash
git add .
git commit -m "Add GitHub Pages deployment"
git push origin main
```

### 3. Wait for Deployment

1. Go to **Actions** tab in your GitHub repo
2. Watch the "Deploy to GitHub Pages" workflow
3. Should complete in ~1-2 minutes

### 4. Visit Your Site

Your site will be live at:
```
https://YOUR_USERNAME.github.io/apiflow/
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## What Gets Deployed

The deployment includes:

```
/
├── index.html                    # Landing page
├── demo-index.html              # Demo showcase
├── demos/                       # All demos
│   ├── dark-pro/
│   ├── light-pro/
│   ├── modern/
│   └── versioning/
├── static/                      # Themes (if needed)
└── CNAME (optional)             # Custom domain
```

**Note:** Python files (`*.py`) and documentation (`*.md`) are included but not executed. They're for reference only.

---

## Custom Domain (Optional)

### Using Your Own Domain

1. **Create CNAME file:**
   ```bash
   echo "docs.yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Configure DNS:**
   Add these DNS records at your domain provider:

   ```
   Type: CNAME
   Name: docs
   Value: YOUR_USERNAME.github.io
   TTL: 3600
   ```

3. **Enable HTTPS:**
   - Go to Settings → Pages
   - Check "Enforce HTTPS"
   - Wait 10-15 minutes for SSL certificate

**Example:** `docs.apiflow.dev` → Landing page

---

## Testing Locally

Before deploying, test your site locally:

### Option 1: Python SimpleHTTPServer
```bash
cd /path/to/apiflow
python3 -m http.server 8000
```
Visit: `http://localhost:8000`

### Option 2: Node.js http-server
```bash
npx http-server -p 8000
```

### Option 3: VS Code Live Server
1. Install "Live Server" extension
2. Right-click `index.html` → "Open with Live Server"

---

## Troubleshooting

### Deployment Failed

**Problem:** Workflow fails with "Pages not enabled"

**Solution:**
1. Go to Settings → Pages
2. Change Source to "GitHub Actions"
3. Re-run the workflow

---

### 404 Error

**Problem:** Site shows 404 on GitHub Pages

**Solution:**
1. Verify `index.html` is in root directory
2. Check file names are lowercase
3. Wait 5 minutes for DNS propagation
4. Clear browser cache

---

### Links Not Working

**Problem:** Demo links are broken

**Solution:**
1. All links should be relative:
   - ✅ `demo-index.html`
   - ✅ `demos/dark-pro/index.html`
   - ❌ `/demo-index.html` (absolute)
   - ❌ `file:///demo-index.html`

2. Update links if needed
3. Test locally first

---

### Custom Domain Not Working

**Problem:** CNAME shows "Not Found"

**Solution:**
1. Verify DNS records are correct
2. Wait 24-48 hours for DNS propagation
3. Use `dig docs.yourdomain.com` to check DNS
4. Ensure CNAME file exists in repository root

---

## CI/CD Pipeline

The deployment workflow:

1. **Trigger:** Automatic on push to `main`
2. **Build:** None needed (static HTML)
3. **Deploy:** Uploads all files to GitHub Pages
4. **Time:** ~1-2 minutes

### Manual Deployment

You can also trigger deployment manually:

1. Go to **Actions** tab
2. Click "Deploy to GitHub Pages"
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"

---

## File Structure for Deployment

```
apiflow/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml        # Deployment workflow
├── demos/                          # Demo pages
│   ├── dark-pro/
│   │   ├── index.html
│   │   ├── css/
│   │   ├── js/
│   │   └── themes/
│   ├── light-pro/
│   ├── modern/
│   └── versioning/
├── index.html                      # Landing page
├── demo-index.html                 # Demo showcase
├── CNAME (optional)                # Custom domain
└── README.md
```

---

## SEO Optimization

### Add Meta Tags

Already included in `index.html`:
```html
<meta name="description" content="...">
<title>ApiFlow - Beautiful API Documentation Generator</title>
```

### Submit to Search Engines

1. **Google Search Console:**
   - https://search.google.com/search-console
   - Add property: `https://YOUR_USERNAME.github.io/apiflow/`
   - Submit sitemap (optional)

2. **Bing Webmaster Tools:**
   - https://www.bing.com/webmasters
   - Add site

---

## Analytics (Optional)

### Add Google Analytics

Add this before `</head>` in `index.html` and `demo-index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Replace `G-XXXXXXXXXX` with your tracking ID.

### Track Conversions

Add event tracking to purchase buttons:

```html
<a href="https://gumroad.com/l/apiflow-pro"
   onclick="gtag('event', 'click_buy_pro', {'event_category': 'conversion'});">
   Buy PRO →
</a>
```

---

## Performance

Your GitHub Pages site is automatically optimized:

✅ **CDN:** Served via GitHub's global CDN
✅ **HTTPS:** Free SSL certificate
✅ **Fast:** No server-side processing
✅ **Reliable:** 99.9% uptime

### Further Optimization

1. **Minify CSS/JS** (optional):
   ```bash
   npm install -g csso-cli uglify-js
   csso demos/dark-pro/css/api-docs.css -o demos/dark-pro/css/api-docs.min.css
   ```

2. **Compress Images** (if you add any):
   - Use TinyPNG or ImageOptim
   - Convert to WebP format

3. **Cache Control:**
   GitHub Pages automatically sets cache headers

---

## Monitoring

### Check Deployment Status

```bash
# View recent deployments
gh workflow view "Deploy to GitHub Pages"

# Watch live deployment
gh run watch
```

### Monitor Traffic

1. GitHub Insights → Traffic
2. Google Analytics (if configured)
3. Gumroad analytics (for sales)

---

## Updating Your Site

To update your live site:

```bash
# Make changes
vim index.html

# Commit and push
git add .
git commit -m "Update pricing"
git push origin main

# Site updates automatically in 1-2 minutes
```

---

## Rollback

If something breaks:

```bash
# Revert to previous commit
git revert HEAD
git push origin main

# Or hard reset (use carefully)
git reset --hard HEAD~1
git push --force origin main
```

---

## Security

### What to Include
✅ HTML, CSS, JS files
✅ Images, fonts
✅ Demo files
✅ Documentation (*.md)

### What NOT to Include
❌ `.env` files
❌ Secret keys
❌ Database credentials
❌ Private customer data
❌ License key generation secrets

**Important:** Never commit sensitive data. Use environment variables for secrets.

---

## Next Steps

After deployment:

1. ✅ Site is live on GitHub Pages
2. ✅ All demos working
3. ✅ Links tested
4. 📱 Test on mobile devices
5. 🔍 Submit to search engines
6. 📣 Share on social media
7. 💰 Start getting sales!

---

## Support

- GitHub Pages Docs: https://docs.github.com/pages
- Custom Domains: https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site
- Troubleshooting: https://docs.github.com/pages/getting-started-with-github-pages/troubleshooting-404-errors-for-github-pages-sites

---

## Checklist

Before going live:

- [ ] GitHub Pages enabled (Settings → Pages → GitHub Actions)
- [ ] Workflow committed and pushed
- [ ] Deployment successful (check Actions tab)
- [ ] Landing page loads (`/index.html`)
- [ ] Demo index loads (`/demo-index.html`)
- [ ] All 4 demos work (dark-pro, light-pro, modern, versioning)
- [ ] All CTA buttons link correctly
- [ ] Gumroad products created
- [ ] Mobile responsive (test on phone)
- [ ] Cross-browser tested (Chrome, Firefox, Safari)
- [ ] Analytics setup (optional)
- [ ] Custom domain configured (optional)

Ready to launch? 🚀
