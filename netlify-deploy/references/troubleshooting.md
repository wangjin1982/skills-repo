# Netlify 部署故障排除指南

本文档包含 Netlify 部署过程中常见问题的解决方案。

## 目录

1. [环境问题](#环境问题)
2. [登录问题](#登录问题)
3. [构建错误](#构建错误)
4. [部署错误](#部署错误)
5. [运行时错误](#运行时错误)

---

## 环境问题

### Netlify CLI 未安装

**错误信息**: `netlify: command not found` 或 `'netlify' 不是内部或外部命令`

**解决方案**:
```bash
npm install -g netlify-cli
```

**验证安装**:
```bash
netlify --version
```

### Node.js 版本过低

**错误信息**: `Engine node is incompatible with this module`

**解决方案**:
- 检查 Node.js 版本: `node --version`
- 升级到 Node.js 18+ (推荐 LTS 版本)
- 使用 nvm 切换版本: `nvm use 18`

---

## 登录问题

### 未登录 Netlify

**错误信息**: `You don't appear to be logged in` 或 `Not logged in`

**解决方案**:
```bash
netlify login
```
这将打开浏览器进行授权登录。

### 登录 Token 过期

**错误信息**: `Authentication failed` 或 `401 Unauthorized`

**解决方案**:
```bash
netlify logout
netlify login
```

---

## 构建错误

### 依赖安装失败

**错误信息**: `npm install failed` 或 `Error: Cannot find module`

**解决方案**:
1. 检查 `package.json` 是否正确
2. 确保 `package-lock.json` 或 `yarn.lock` 已提交
3. 在本地先测试构建: `npm run build`
4. 检查 Node.js 版本是否匹配

### 内存不足

**错误信息**: `JavaScript heap out of memory`

**解决方案**:
在 `netlify.toml` 中增加内存限制:
```toml
[build.environment]
  NODE_OPTIONS = "--max-old-space-size=4096"
```

### 构建超时

**错误信息**: `Build exceeded maximum allowed runtime`

**解决方案**:
1. 优化构建过程（移除不必要的依赖）
2. 使用构建缓存
3. 考虑升级 Netlify 套餐（免费版有 15 分钟限制）

---

## 部署错误

### 未指定 Publish 目录

**错误信息**: `No publish directory configured` 或 `Publish directory not found`

**解决方案**:
在 `netlify.toml` 中指定正确的输出目录:

- Next.js: `.next` (需要 @netlify/plugin-nextjs)
- React/Vite: `dist`
- Create React App: `build`
- Vue: `dist`

```toml
[build]
  publish = ".next"
```

### 站点未链接

**错误信息**: `This folder isn't linked to a project yet`

**解决方案**:
方法 1 - 自动创建:
```bash
netlify deploy --prod
```
然后选择 "Create & configure a new project"

方法 2 - 使用提供的脚本:
```bash
python scripts/create_site.py
```

方法 3 - 链接现有站点:
```bash
netlify link
```

---

## 运行时错误

### 环境变量未配置

**错误信息**: API 调用失败或功能异常

**解决方案**:
1. 在 Netlify Dashboard 配置环境变量:
   - 访问: `Site settings > Environment variables`
   - 添加所需的环境变量
2. 或在 `netlify.toml` 中配置（不推荐敏感信息）:
```toml
[build.environment]
  NODE_ENV = "production"
```

### 函数调用失败

**错误信息**: `Function invocation failed` 或 `502 Bad Gateway`

**解决方案**:
1. 检查函数日志: `Site > Functions > Logs`
2. 确保函数超时设置合理
3. 检查函数依赖是否正确安装

### Next.js 动态路由 404

**错误信息**: 刷新页面显示 404

**解决方案**:
确保使用了 `@netlify/plugin-nextjs` 插件:
```toml
[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### CORS 错误

**错误信息**: `Access to fetch blocked by CORS policy`

**解决方案**:
在 `netlify.toml` 中配置 CORS 头:
```toml
[[headers]]
  for = "/api/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, POST, PUT, DELETE, OPTIONS"
    Access-Control-Allow-Headers = "Content-Type"
```

---

## 调试技巧

### 1. 查看详细日志

```bash
netlify deploy --prod --debug
```

### 2. 本地测试构建

```bash
# 测试构建命令
npm run build

# 测试 Netlify 构建
netlify build
```

### 3. 使用 Netlify Dev

在本地模拟 Netlify 环境:
```bash
netlify dev
```

### 4. 查看部署日志

- 访问: `https://app.netlify.com/sites/[site-name]/deploys`
- 点击失败的部署查看详细日志

---

## 常见配置检查清单

- [ ] `netlify.toml` 文件存在且配置正确
- [ ] Build command 正确（如 `npm run build`）
- [ ] Publish directory 正确（如 `.next`, `dist`, `build`）
- [ ] 必要的插件已配置（如 Next.js 需要 `@netlify/plugin-nextjs`）
- [ ] 环境变量已在 Netlify Dashboard 配置
- [ ] 本地构建成功 (`npm run build`)
- [ ] Netlify CLI 已安装并登录
- [ ] Node.js 版本满足要求

---

## 获取帮助

如果问题仍未解决:
1. 查看 [Netlify 官方文档](https://docs.netlify.com/)
2. 访问 [Netlify 社区论坛](https://answers.netlify.com/)
3. 检查 [Netlify 状态页面](https://www.netlifystatus.com/) 确认服务是否正常
