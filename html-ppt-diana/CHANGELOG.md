# Changelog - HTML PPT Diana Skill

## [2026-01-14] - Mermaid 渲染问题修复与离线支持

### 🔧 核心修复

#### 问题描述
- Mermaid 流程图和甘特图在生成的 HTML PPT 中无法渲染
- 显示为原始 Mermaid 语法文本而非图形化展示

#### 根本原因
1. ES6 模块导入在 `startOnLoad: true` 模式下初始化时机不当
2. 隐藏的 slide 元素（`display: none`）渲染时尺寸计算错误
3. jsdelivr CDN 在部分网络环境下访问不稳定

### ✅ 解决方案

#### 1. CDN 替换
**文件：** `assets/ppt-template/index.html`

**修改前：**
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true, ... });
</script>
```

**修改后：**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.6.1/mermaid.min.js" defer></script>
```

**优势：**
- cdnjs 全球 CDN 可用性更高
- 使用 `defer` 确保 DOM 就绪后加载
- 传统全局变量方式更兼容

#### 2. 初始化策略优化
**文件：** `assets/ppt-template/presentation.js`

**关键变更：**
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // Mermaid 初始化移到这里，避免在 slide 隐藏时渲染
    if (typeof mermaid !== 'undefined' && typeof mermaid.initialize === 'function') {
        mermaid.initialize({
            startOnLoad: false,  // ⚠️ 关键：禁用自动渲染
            theme: 'default',
            securityLevel: 'loose',
            themeVariables: { fontSize: '16px' },
            flowchart: { useMaxWidth: true, htmlLabels: true },
            gantt: { useMaxWidth: true }
        });
    }

    window.presentation = new Presentation();
});
```

#### 3. 按需渲染机制
**文件：** `assets/ppt-template/presentation.js` (presentation.js:137-146)

**新增代码：**
```javascript
updateDisplay() {
    // ... 其他更新逻辑

    // 只渲染当前可见 slide 中的 Mermaid 图表
    const currentSlideElement = this.slides[this.currentSlide];
    const mermaidElements = currentSlideElement.querySelectorAll('.mermaid:not([data-processed])');
    if (mermaidElements.length > 0 && typeof mermaid !== 'undefined') {
        if (typeof mermaid.run === 'function') {
            mermaid.run({ nodes: mermaidElements });  // v10+ 推荐方法
        } else if (typeof mermaid.init === 'function') {
            mermaid.init(undefined, mermaidElements); // 向下兼容
        }
    }

    // ... ECharts 调整
}
```

**技术要点：**
- `:not([data-processed])` 避免重复渲染
- 优先使用 Mermaid v10 的 `run()` 方法
- 向下兼容 v9 的 `init()` 方法

### 📚 新增文档

#### 1. `references/mermaid-fix.md`
详细的 Mermaid 渲染问题修复方案，包含：
- 问题描述与根本原因分析
- CDN 替换方案（jsdelivr → cdnjs）
- 初始化策略（`startOnLoad: false`）
- 按需渲染机制（翻页时触发）
- 正确做法 vs 错误做法对比
- 浏览器兼容性说明

#### 2. `references/offline-setup.md`
完整的离线部署指南，包含：
- 静态资源下载方法（手动/命令行）
- HTML 引用路径修改
- 自动化脚本（Bash / PowerShell）
- 文件大小参考（~5.2MB）
- 打包分发方法
- CDN vs 离线方案对比
- 疑难排查与版本更新

### 📝 文档更新

#### `skill.md` 主文档
**更新内容：**
1. Overview 部分强调"已优化渲染策略"和"离线环境支持"
2. Troubleshooting 部分重写"流程图不渲染"条目，添加修复说明
3. 新增"离线环境无法使用"问题排查
4. Resources 部分添加新文档引用

### 🎯 效果验证

**测试场景：**
- ✅ 流程图（graph TB/LR）正常渲染
- ✅ 甘特图（gantt）正常显示
- ✅ 翻页时图表动态加载
- ✅ 多次翻页不重复渲染
- ✅ 离线环境下（配置后）正常使用

**浏览器兼容：**
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

### 🔄 迁移指南

**已有项目如何升级：**

1. **替换核心文件：**
```bash
# 备份旧文件
cp presentation.js presentation.js.backup

# 从 Skill 模板复制新版本
cp {skill_dir}/assets/ppt-template/presentation.js .
```

2. **更新 HTML CDN 引用：**
```bash
# 修改 index.html 中的 CDN 引用
# 从 jsdelivr 改为 cdnjs
# 移除 ES6 模块导入，使用传统 script 标签
```

3. **测试验证：**
```bash
# 在浏览器中打开
# 测试 Mermaid 图表是否正常显示
```

### 📊 性能影响

- **加载速度：** 相同（CDN 切换无明显差异）
- **渲染性能：** 提升（按需渲染减少初始开销）
- **内存占用：** 优化（避免隐藏元素渲染）
- **离线支持：** 文件增加 ~5.2MB（可选）

### 🚀 未来计划

- [ ] 考虑集成更多 Mermaid 图表类型（序列图、类图等）
- [ ] 提供一键下载离线资源的脚本
- [ ] 探索 Mermaid 本地渲染优化（WebWorker）
- [ ] 添加图表主题定制功能

### 👏 致谢

感谢用户反馈的 Mermaid 渲染问题，通过实际场景测试找到了最优解决方案。

---

**版本：** 1.1.0
**日期：** 2026-01-14
**维护者：** Diana Skill Team
