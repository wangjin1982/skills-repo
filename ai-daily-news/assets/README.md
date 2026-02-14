# Assets 目录说明

此目录用于存放AI日报生成所需的静态资源文件。

## 微信二维码图片

### 文件命名
- `weixin_qr.png` (推荐)
- `weixin_qr.jpg`
- `weixin_qr.gif`

### 使��说明
1. 将您的微信公众号二维码图片放入此目录
2. 命名为 `weixin_qr.png` 或 `weixin_qr.jpg`
3. 运行AI日报生成脚本时，程序会自动查找并嵌入此二维码

### 图片要求
- **格式**: PNG、JPG 或 GIF
- **尺寸**: 建议正方形（如 200x200 像素）
- **内容**: 清晰可识别的微信公众号二维码
- **文件大小**: 建议小于 500KB

### 如果不提供二维码
如果没有放置二维码图片，日报将显示默认的手机图标占位符。

### 自定义二维码路径
如果您想使用其他路径的二维码，可以在运行时指定：
```bash
python scripts/generate_report.py news.json report.html --qr-code /path/to/your/qrcode.jpg
```

## 示例
```
assets/
├── README.md (本文件)
└── weixin_qr.png (您的微信二维码)
```
