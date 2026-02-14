# 框架配置指南

本文档提供不同前端框架的 Netlify 部署配置示例。

## 目录

- [Next.js](#nextjs)
- [React (Create React App)](#react-create-react-app)
- [React (Vite)](#react-vite)
- [Vue.js](#vuejs)
- [Nuxt.js](#nuxtjs)
- [Svelte/SvelteKit](#sveltesveltekit)
- [静态 HTML](#静态-html)
- [Astro](#astro)

---

## Next.js

### 配置文件: `netlify.toml`

```toml
[build]
  command = "npm run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"

# 环境变量（示例，实际应在 Dashboard 配置）
# [build.environment]
#   NODE_ENV = "production"
```

### 关键点

- ✅ **必须安装插件**: `@netlify/plugin-nextjs`
- ✅ **Publish 目录**: `.next`
- ✅ **支持**: SSR, ISR, API Routes, 动态路由
- ✅ **Node.js 版本**: 18+ 推荐

### 安装插件

如果项目中未安装，需要添加:
```bash
npm install -D @netlify/plugin-nextjs
```

---

## React (Create React App)

### 配置文件: `netlify.toml`

```toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 关键点

- ✅ **Publish 目录**: `build`
- ✅ **SPA 路由**: 需要配置 redirects（见上方）
- ⚠️ **环境变量前缀**: 必须以 `REACT_APP_` 开头

---

## React (Vite)

### 配置文件: `netlify.toml`

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 关键点

- ✅ **Publish 目录**: `dist`
- ✅ **构建命令**: `npm run build` 或 `vite build`
- ✅ **环境变量前缀**: `VITE_`

---

## Vue.js

### Vue CLI

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Vite (Vue 3)

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 关键点

- ✅ **Publish 目录**: `dist`
- ✅ **环境变量**: Vue CLI 使用 `VUE_APP_`, Vite 使用 `VITE_`

---

## Nuxt.js

### Nuxt 3

```toml
[build]
  command = "npm run build"
  publish = ".output/public"

[[redirects]]
  from = "/_nuxt/*"
  to = "/_nuxt/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Nuxt 2

```toml
[build]
  command = "npm run generate"
  publish = "dist"
```

### 关键点

- ✅ **Nuxt 3**: 使用 `npm run build`, publish `.output/public`
- ✅ **Nuxt 2**: 使用 `npm run generate`, publish `dist`
- ✅ **SSR**: Nuxt 3 支持 Netlify Functions 实现 SSR

---

## Svelte/SvelteKit

### SvelteKit

```toml
[build]
  command = "npm run build"
  publish = "build"

[[plugins]]
  package = "@sveltejs/adapter-netlify"
```

### Svelte (Vite)

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 关键点

- ✅ **SvelteKit**: 需要使用 `@sveltejs/adapter-netlify`
- ✅ **Publish 目录**: SvelteKit 为 `build`, Vite 为 `dist`

---

## 静态 HTML

### 配置文件: `netlify.toml`

```toml
[build]
  command = "echo 'No build command required'"
  publish = "."

# 或者如果有特定的静态文件目录
# [build]
#   publish = "public"
```

### 关键点

- ✅ **无需构建**: 直接部署 HTML/CSS/JS 文件
- ✅ **Publish 目录**: 指向包含 `index.html` 的目录

---

## Astro

### 配置文件: `netlify.toml`

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 关键点

- ✅ **Publish 目录**: `dist`
- ✅ **SSR 支持**: 需要配置 Astro 的 Netlify adapter
- ✅ **静态生成**: 默认配置即可

---

## 通用配置选项

### 环境变量

在 `netlify.toml` 中配置（非敏感信息）:
```toml
[build.environment]
  NODE_VERSION = "18"
  NODE_ENV = "production"
```

在 Netlify Dashboard 中配置（敏感信息）:
- Site settings > Environment variables
- 添加 key-value 对

### 构建缓存

启用缓存以加速构建:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.processing]
  skip_processing = false
```

### 自定义头部

```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
```

### 重定向和重写

```toml
# SPA 路由重定向
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# API 代理
[[redirects]]
  from = "/api/*"
  to = "https://api.example.com/:splat"
  status = 200
```

---

## 自动检测框架

Netlify 可以自动检测常见框架并应用默认配置。如果自动检测失败，可以手动创建 `netlify.toml`。

**支持自动检测的框架**:
- Next.js
- Create React App
- Vue CLI
- Nuxt
- Gatsby
- Hugo
- Jekyll
- 等等...

---

## 检测项目框架

查看 `package.json` 中的依赖和脚本:

```bash
# Next.js
"dependencies": { "next": "..." }
"scripts": { "build": "next build" }

# React (CRA)
"dependencies": { "react-scripts": "..." }
"scripts": { "build": "react-scripts build" }

# React (Vite)
"devDependencies": { "vite": "..." }
"scripts": { "build": "vite build" }

# Vue
"dependencies": { "vue": "..." }
"devDependencies": { "@vue/cli-service": "..." } # Vue CLI
"devDependencies": { "vite": "..." } # Vite
```

---

## 部署前检查清单

- [ ] 本地构建成功 (`npm run build`)
- [ ] `package.json` 包含正确的 build 脚本
- [ ] `netlify.toml` 配置正确（如果需要）
- [ ] 必要的插件已安装
- [ ] 环境变量已配置（Dashboard 或 netlify.toml）
- [ ] Publish 目录路径正确
- [ ] Node.js 版本要求明确
