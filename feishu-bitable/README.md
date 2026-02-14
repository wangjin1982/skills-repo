# 飞书多维表格 Skill - 使用指南

## ⚠️ 重要提示

### 1. 空记录问题
写入数据后，飞书系统会自动生成约10行空记录。详见 [KNOWN_ISSUES.md](KNOWN_ISSUES.md)。

### 2. 权限问题（部分解决）
- **当前状态**：机器人创建的多维表格默认只属于机器人
- **解决方案**：在飞书中手动设置"分享"权限为"可编辑"
- **详细说明**：见 [PERMISSION_GUIDE.md](PERMISSION_GUIDE.md)

**快速设置权限：**
1. 打开机器人创建的多维表格链接
2. 点击右上角"分享"
3. 设置为"互联网获得链接的任何人"
4. 权限选择"可编辑"

---

## 快速开始

### 1. 基本用法

```python
from feishu_bitable_manager import create_manager

# 创建管理器
manager = create_manager(
    app_id="your_app_id",
    app_secret="your_app_secret"
)

# 导入CSV到多维表格
result = manager.import_csv_to_bitable(
    csv_file="/path/to/data.csv",
    table_name="我的数据表"
)

print(f"✅ 导入成功！")
print(f"📊 链接: {result['url']}")
print(f"📈 记录数: {result['written']}")
```

### 2. 高级用法 - 分步操作

```python
# 创建应用
app_token = manager.create_app("数据表名称")

# 获取默认数据表
table_id, table_name = manager.get_default_table(app_token)

# 清理现有数据
deleted = manager.delete_all_records(app_token, table_id)
print(f"删除了 {deleted} 条旧记录")

# 删除模板字段
deleted_fields = manager.delete_template_fields(app_token, table_id)
print(f"删除了 {deleted_fields} 个模板字段")

# 创建业务字段
field_names = ["姓名", "年龄", "城市"]
created = manager.create_business_fields(app_token, table_id, field_names)
print(f"创建了 {created} 个业务字段")

# 写入数据
records = [
    {"fields": {"姓名": "张三", "年龄": "25", "城市": "北京"}},
    {"fields": {"姓名": "李四", "年龄": "30", "城市": "上海"}}
]
written = manager.write_records(app_token, table_id, records)
print(f"写入了 {written} 条记录")

# 验证数据
verification = manager.verify_data(app_token, table_id)
print(f"验证: {verification['business']} 条业务记录")

# 清理空记录和重复记录
cleanup = manager.cleanup_data(app_token, table_id)
print(f"清理: {cleanup['empty']} 条空记录, {cleanup['duplicates']} 条重复记录")
```

## API 参考

### FeishuBitableManager

#### 方法

##### `create_app(name: str) -> str`
创建多维表格应用

**参数:**
- `name`: 应用名称

**返回:**
- `app_token`: 应用令牌

##### `get_default_table(app_token: str) -> tuple`
获取默认数据表

**参数:**
- `app_token`: 应用令牌

**返回:**
- `(table_id, table_name)`: 数据表ID和名称

##### `delete_all_records(app_token: str, table_id: str) -> int`
删除所有记录

**参数:**
- `app_token`: 应用令牌
- `table_id`: 数据表ID

**返回:**
- 删除的记录数

##### `delete_template_fields(app_token: str, table_id: str) -> int`
删除模板字段

**参数:**
- `app_token`: 应用令牌
- `table_id`: 数据表ID

**返回:**
- 删除的字段数

##### `create_business_fields(app_token: str, table_id: str, field_names: List[str]) -> int`
创建业务字段

**参数:**
- `app_token`: 应用令牌
- `table_id`: 数据表ID
- `field_names`: 字段名列表

**返回:**
- 创建的字段数

##### `write_records(app_token: str, table_id: str, records: List[Dict]) -> int`
批量写入记录

**参数:**
- `app_token`: 应用令牌
- `table_id`: 数据表ID
- `records`: 记录列表

**返回:**
- 写入的记录数

##### `cleanup_data(app_token: str, table_id: str) -> Dict`
清理数据：删除空记录和重复记录

**参数:**
- `app_token`: 应用令牌
- `table_id`: 数据表ID

**返回:**
- 清理统计信息 `{"empty": int, "duplicates": int}`

##### `verify_data(app_token: str, table_id: str) -> Dict`
验证数据

**参数:**
- `app_token`: 应用令牌
- `table_id`: 数据表ID

**返回:**
- 验证结果 `{"success": bool, "total": int, "business": int, "first_record": dict}`

##### `import_csv_to_bitable(csv_file: str, table_name: str) -> Dict`
将CSV文件导入到飞书多维表格（完整流程）

**参数:**
- `csv_file`: CSV文件路径
- `table_name`: 表格名称

**返回:**
- 导入结果 `{"success": bool, "app_token": str, "table_id": str, "url": str, "written": int, "verified": int}`

## 最佳实践

### 1. 一次性导入（推荐）

```python
# 最简单的方式，自动处理所有清理工作
result = manager.import_csv_to_bitable("data.csv", "我的数据")
```

### 2. 批量导入多个CSV

```python
csv_files = [
    ("data1.csv", "数据表1"),
    ("data2.csv", "数据表2"),
    ("data3.csv", "数据表3")
]

for csv_file, table_name in csv_files:
    result = manager.import_csv_to_bitable(csv_file, table_name)
    print(f"✅ {table_name}: {result['url']}")
```

### 3. 错误处理

```python
try:
    result = manager.import_csv_to_bitable("data.csv", "我的数据")
    if result['success']:
        print(f"✅ 成功！链接: {result['url']}")
    else:
        print(f"❌ 失败: {result.get('error')}")
except Exception as e:
    print(f"❌ 异常: {e}")
```

## 常见问题

### Q: 为什么会有空记录？
A: **这是飞书系统的已知行为**。写入数据后，飞书会自动在前面生成约10行空记录。这是飞书平台的机制，Skill无法从API层面完全消除。

**说明：**
- Skill会尝试清理这些空记录
- 但飞书系统可能会重新生成
- 业务数据本身是完整和正确的
- 建议在飞书前端界面查看数据（可能自动过滤了空记录）

### Q: 如何避免重复记录？
A: 每次导入前会删除所有现有记录。如果需要增量导入，请先检查记录是否存在。

### Q: 字段名有限制吗？
A: 字段名不能包含特殊字符，建议使用中文、英文、数字和下划线。

### Q: 一次最多可以导入多少条记录？
A: 建议每次不超过500条，超过请分批导入。

### Q: 为什么验证的记录数和写入的不一样？
A: 如果验证的记录数多于写入数，说明有空记录。这是飞书系统行为，不影响业务数据。

## 配置

### 环境变量

```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

### 代码中配置

```python
manager = create_manager(
    app_id="cli_a9d176668a38dbc9",
    app_secret="jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T"
)
```

## 示例

### 示例1：导入销售数据

```python
sales_data = [
    {"产品": "A", "销量": 100, "金额": 1000},
    {"产品": "B", "销量": 200, "金额": 2000}
]

manager = create_manager(app_id, app_secret)
app_token = manager.create_app("销售数据")
table_id, _ = manager.get_default_table(app_token)

manager.delete_all_records(app_token, table_id)
manager.delete_template_fields(app_token, table_id)
manager.create_business_fields(app_token, table_id, ["产品", "销量", "金额"])
manager.write_records(app_token, table_id, [{"fields": row} for row in sales_data])
```

### 示例2：清理和验证

```python
# 清理数据
cleanup = manager.cleanup_data(app_token, table_id)
print(f"删除了 {cleanup['empty']} 条空记录")
print(f"删除了 {cleanup['duplicates']} 条重复记录")

# 验证数据
verification = manager.verify_data(app_token, table_id)
print(f"总计: {verification['total']} 条")
print(f"业务数据: {verification['business']} 条")
print(f"第一条: {verification['first_record']}")
```

## 技术支持

如有问题，请参考：
- skill.md：完整的Skill文档
- feishu_bitable_manager.py：源代码和注释
