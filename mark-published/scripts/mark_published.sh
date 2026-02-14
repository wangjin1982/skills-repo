#!/bin/bash

# 标记公众号文章为已发布
# 用法: scripts/mark_published.sh

# 设置目录路径
VAULT_ROOT="/Users/jackywang/Documents/学习笔记/学习笔记"
ARTICLE_DIR="${VAULT_ROOT}/公众号文章"

# 统计变量
total_count=0
marked_count=0
skipped_count=0

echo "开始处理公众号文章..."
echo "文章目录: ${ARTICLE_DIR}"
echo ""

# 遍历公众号文章文件夹下的所有 md 文件
for file in "${ARTICLE_DIR}"/*.md; do
    # 跳过不存在的文件
    [ -f "$file" ] || continue

    # 获取文件名
    filename=$(basename "$file")
    total_count=$((total_count + 1))

    # 检查是否已包含【已发布】
    if [[ "$filename" == 【已发布】* ]]; then
        echo "⊘ 跳过: $filename (已标记)"
        skipped_count=$((skipped_count + 1))
    else
        # 重命名文件，添加【已发布】前缀
        new_name="${ARTICLE_DIR}/【已发布】${filename}"
        mv "$file" "$new_name"
        echo "✓ 标记: $filename → 【已发布】${filename}"
        marked_count=$((marked_count + 1))
    fi
done

echo ""
echo "===================="
echo "处理完成！"
echo "共处理: ${total_count} 篇文章"
echo "新增标记: ${marked_count} 篇"
echo "已跳过: ${skipped_count} 篇"
echo "===================="

# 返回结果供钉钉通知使用
echo "RESULT: total=${total_count}, marked=${marked_count}, skipped=${skipped_count}"
