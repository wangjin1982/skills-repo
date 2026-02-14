---
name: netlify-deploy
description: Automate deployment of code projects to Netlify platform with complete build process, error debugging, and live URL delivery. Use when user requests deploying to Netlify, needs help with Netlify deployment, wants to publish a website/app to Netlify, or encounters Netlify deployment issues. Supports Next.js, React, Vue, Svelte, static sites, and more. Handles CLI setup, site creation, build configuration, deployment execution, and troubleshooting.
---

# Netlify Deployment Automation

Automate the complete deployment workflow for web projects to Netlify, including environment setup, configuration, building, debugging, and delivering the live URL.

## Quick Start

### Deployment Workflow

Execute these steps in order:

1. **Environment Check**
   ```bash
   python scripts/check_env.py
   ```
   Verifies Netlify CLI installation and login status.

2. **Detect Framework**
   Read `package.json` to identify the project framework (Next.js, React, Vue, etc.).

3. **Configure Build**
   - Check for existing `netlify.toml`
   - If missing, use appropriate template from `assets/templates/`
   - Verify build command and publish directory are correct

4. **Create/Link Site**
   - If site not linked:
     ```bash
     python scripts/create_site.py
     ```
   - Or manually via Netlify API

5. **Deploy**
   ```bash
   netlify deploy --prod
   ```

6. **Deliver Results**
   - Extract and present the deployment URL
   - Provide admin dashboard link
   - Confirm successful deployment

## Framework Detection

Identify framework from `package.json` dependencies:

| Framework | Dependency | Build Command | Publish Dir |
|-----------|------------|---------------|-------------|
| Next.js | `"next"` | `npm run build` | `.next` |
| React (CRA) | `"react-scripts"` | `react-scripts build` | `build` |
| React (Vite) | `"vite"` + `"react"` | `vite build` | `dist` |
| Vue | `"vue"` | `npm run build` | `dist` |
| Svelte | `"svelte"` | `npm run build` | `dist` |

For detailed framework configurations, see [framework_configs.md](references/framework_configs.md).

## Configuration Templates

Use templates from `assets/templates/` based on detected framework:
- `nextjs.toml` - Next.js projects
- `react-vite.toml` - React with Vite
- `react-cra.toml` - Create React App
- `vue.toml` - Vue projects

Copy the appropriate template to the project root as `netlify.toml` if it doesn't exist.

## Environment Setup

### Prerequisites Check

Use `scripts/check_env.py` to verify:
- ✅ Netlify CLI installed (`netlify-cli`)
- ✅ User logged in via `netlify login`
- ✅ Site linked (or ready to create new site)

If CLI not installed:
```bash
npm install -g netlify-cli
```

If not logged in:
```bash
netlify login
```

## Site Creation

### Automatic Creation

Use the provided script:
```bash
python scripts/create_site.py [--name site-name]
```

This will:
1. Create a new Netlify site via API
2. Link the current directory to the site
3. Create `.netlify/state.json` with site ID

### Manual Creation

Via Netlify API:
```bash
netlify api createSite --data '{"body":{"name":"my-site"}}'
```

Then link manually by creating `.netlify/state.json`:
```json
{
  "siteId": "your-site-id-here"
}
```

## Build Configuration

### Next.js Specific

- **Required plugin**: `@netlify/plugin-nextjs`
- Install if missing:
  ```bash
  npm install -D @netlify/plugin-nextjs
  ```
- Publish directory: `.next`
- Supports SSR, ISR, API Routes

### SPA Projects (React, Vue)

Requires redirect configuration for client-side routing:
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Deployment Process

### Standard Deployment

```bash
netlify deploy --prod
```

This command:
1. Runs the build command
2. Packages the output directory
3. Uploads to Netlify
4. Returns deployment URL

### Draft Deployment (Preview)

```bash
netlify deploy
```

Creates a preview deployment without affecting production.

## Error Handling

When deployment fails, diagnose using the error message:

**Common Issues**:
- CLI not installed → Install `netlify-cli`
- Not logged in → Run `netlify login`
- Build failure → Check build logs, verify local build works
- Missing config → Create `netlify.toml` from templates
- Site not linked → Run `scripts/create_site.py`

For comprehensive troubleshooting, see [troubleshooting.md](references/troubleshooting.md).

## Debug Mode

Enable detailed logging:
```bash
netlify deploy --prod --debug
```

## Environment Variables

Configure sensitive environment variables in Netlify Dashboard:
1. Site settings > Environment variables
2. Add key-value pairs
3. Redeploy for changes to take effect

Non-sensitive variables can go in `netlify.toml`:
```toml
[build.environment]
  NODE_VERSION = "18"
```

## Post-Deployment

After successful deployment, provide user with:
- ✅ **Production URL**: `https://[site-name].netlify.app`
- ✅ **Unique deploy URL**: `https://[deploy-id]--[site-name].netlify.app`
- ✅ **Admin dashboard**: `https://app.netlify.com/sites/[site-name]`
- ✅ **Build logs link**: For debugging if needed

## Result Delivery

Present deployment results in a clear, structured format:

```
🎉 Deployment Successful!

📋 Deployment Information
├─ Production URL: https://your-site.netlify.app
├─ Admin Dashboard: https://app.netlify.com/sites/your-site
└─ Build Time: X.Xs

✅ Next Steps
- Visit your site at the URL above
- Configure environment variables if needed
- Set up custom domain (optional)
```

## Reference Documents

- **[troubleshooting.md](references/troubleshooting.md)** - Common errors and solutions
- **[framework_configs.md](references/framework_configs.md)** - Detailed configuration for each framework

## Scripts

- **`scripts/check_env.py`** - Check Netlify CLI and login status
- **`scripts/create_site.py`** - Create and link a new Netlify site

## Complete Example Workflow

```bash
# 1. Check environment
python scripts/check_env.py

# 2. Create site (if needed)
python scripts/create_site.py

# 3. Verify netlify.toml exists (create from template if needed)
# [Manual step or automated based on framework detection]

# 4. Deploy
netlify deploy --prod

# 5. Extract and present deployment URL
```

---

## Notes

- Always verify local build succeeds before deploying: `npm run build`
- For large projects, consider enabling build caching
- Next.js projects require the `@netlify/plugin-nextjs` plugin
- SPA projects need redirect configuration for routing to work
- Environment variables for API keys should be set in Dashboard, not `netlify.toml`
