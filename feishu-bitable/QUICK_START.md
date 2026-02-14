# 飞书多维表格 Skill - 快速开始

## ⚠️ 重要提示

在使用本Skill之前，请务必了解以下**已知问题**：

### 空记录问题（未解决）
- 写入数据后，飞书系统会自动在前面生成约10行空记录
- 这是飞书平台的系统行为，Skill无法从API层面完全解决
- **不影响业务数据的完整性和正确性**
- 详见 `KNOWN_ISSUES.md` 文件

## 快速使用

```python
from feishu_bitable_manager import create_manager

# 1. 创建管理器
manager = create_manager(
    app_id="your_app_id",
    app_secret="your_app_secret"
)

# 2. 导入CSV（最简单）
result = manager.import_csv_to_bitable(
    csv_file="data.csv",
    table_name="我的数据表"
)

# 3. 查看结果
print(f"✅ 成功！")
print(f"链接: {result['url']}")
print(f"写入: {result['written']} 条业务记录")
print(f"验证: {result['verified']} 条业务记录（排除空记录）")
print(f"清理: {result['cleanup']['empty']} 条空记录")
```

## 返回值说明

```python
{
    "success": True,                    # 是否成功
    "app_token": "xxx",                 # 应用令牌
    "table_id": "xxx",                  # 数据表ID
    "url": "https://feishu.cn/base/xxx", # 多维表格链接
    "written": 5,                       # 写入的业务记录数
    "verified": 5,                      # 验证的业务记录数（排除空记录）
    "cleanup": {
        "empty": 10,                    # 清理的空记录数
        "duplicates": 0                 # 清理的重复记录数
    }
}
```

## 理解空记录问题

**示例场景：**
```
写入5条业务记录
→ 飞书系统自动生成10条空记录
→ Skill清理10条空记录
→ 飞书系统又生成10条空记录（系统行为）
→ 最终：15条记录（5条业务 + 10条空）
```

**关键点：**
- `written = 5`：你的业务数据，完整正确
- `verified = 5`：Skill验证的业务记录数
- `total = 15`：API返回的总数（包含空记录）
- **业务数据本身没有问题**

## 建议

1. **接受此限制**：这是飞书平台的行为，Skill无法解决
2. **关注业务数据**：`verified` 字段显示实际业务记录数
3. **前端查看**：在飞书前端界面查看（可能自动过滤）
4. **手动清理**：如果需要，在飞书前端手动删除空记录

## 完整文档

- `skill.md` - 完整Skill文档
- `README.md` - 详细使用指南
- `KNOWN_ISSUES.md` - 已知问题详细说明
- `example.py` - 使用示例

---

**重要**：使用前请确保已了解并接受空记录问题。
