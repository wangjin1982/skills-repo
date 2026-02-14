#!/usr/bin/env python3
"""
火车票发票合并脚本
功能：从ZIP文件中提取发票PDF，按时间排序，合并成每页2张的打印友好PDF
"""

import os
import re
import zipfile
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from io import BytesIO

# 配置
INVOICES_PER_PAGE = 2
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 15  # 边距（points）


def extract_zips(directory="."):
    """解压所有ZIP文件到临时目录"""
    temp_dir = tempfile.mkdtemp(prefix="train_invoices_")
    zip_files = list(Path(directory).glob("*.zip"))
    print(f"   找到 {len(zip_files)} 个ZIP文件")

    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            zf.extractall(temp_dir)
            print(f"   - 已解压: {zip_file.name}")

    return temp_dir, len(zip_files)


def extract_date_from_pdf(pdf_path):
    """从PDF中提取乘车日期"""
    try:
        doc = fitz.open(pdf_path)
        if len(doc) > 0:
            page = doc[0]
            text = page.get_text()

            # 尝试匹配"2026年01月06日"这样的格式
            pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
            match = re.search(pattern, text)
            if match:
                year, month, day = match.groups()
                doc.close()
                return datetime(int(year), int(month), int(day))

        doc.close()
        return datetime.min
    except Exception as e:
        print(f"   警告: 提取日期失败 {pdf_path}: {e}")
        return datetime.min


def extract_invoice_info(pdf_path):
    """从PDF中提取完整发票信息"""
    try:
        doc = fitz.open(pdf_path)
        if len(doc) > 0:
            page = doc[0]
            text = page.get_text()

            # 提取发票号码
            invoice_no_match = re.search(r'发票号码[：:\s]*(\d+)', text)
            invoice_no = invoice_no_match.group(1) if invoice_no_match else Path(pdf_path).stem

            # 提取乘车日期
            travel_date = extract_date_from_pdf(pdf_path)

            # 提取票价
            price_match = re.search(r'票价[：:\s]*￥?(\d+\.?\d*)', text)
            price = price_match.group(1) if price_match else '未知'

            # 提取车次
            train_match = re.search(r'[A-Z]\d+[A-Z]?', text)
            train_no = train_match.group(0) if train_match else '未知'

            doc.close()
            return {
                'path': pdf_path,
                'filename': Path(pdf_path).name,
                'invoice_no': invoice_no,
                'travel_date': travel_date,
                'price': price,
                'train_no': train_no
            }
    except Exception as e:
        print(f"   警告: 无法处理 {pdf_path}: {e}")
    return None


def collect_and_sort_invoices(temp_dir):
    """收集并排序发票信息"""
    pdf_files = sorted(Path(temp_dir).glob("*.pdf"))
    invoices = []

    for pdf_file in pdf_files:
        info = extract_invoice_info(pdf_file)
        if info:
            invoices.append(info)

    # 按乘车日期排序
    invoices.sort(key=lambda x: x['travel_date'] if x['travel_date'] != datetime.min else datetime.max)
    return invoices


def pdf_to_image(pdf_path, page_num=0, zoom=3):
    """将PDF页面转换为高质量图像"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    doc.close()
    return img_data


def create_merged_pdf(invoices, output_path):
    """创建合并后的PDF，每页2张发票"""
    c = canvas.Canvas(output_path, pagesize=A4)

    # 计算每张发票的可用空间
    ticket_height = (PAGE_HEIGHT - 3 * MARGIN) / INVOICES_PER_PAGE
    ticket_width = PAGE_WIDTH - 2 * MARGIN

    for i, invoice in enumerate(invoices):
        position = i % INVOICES_PER_PAGE

        # 计算在页面上的位置
        if position == 0:  # 上一张票
            y_offset = PAGE_HEIGHT - MARGIN - ticket_height
        else:  # 下一张票
            y_offset = MARGIN

        x_offset = MARGIN

        # 将PDF转换为图像并绘制
        img_data = pdf_to_image(invoice['path'])
        img_reader = ImageReader(BytesIO(img_data))

        # 获取原始图片尺寸
        img_width, img_height = img_reader.getSize()

        # 计算缩放比例（保持宽高比）
        scale = min(ticket_width / img_width, ticket_height / img_height)

        draw_width = img_width * scale
        draw_height = img_height * scale

        # 居中显示
        x_centered = x_offset + (ticket_width - draw_width) / 2
        y_centered = y_offset + (ticket_height - draw_height) / 2

        c.drawImage(img_reader, x_centered, y_centered,
                   draw_width, draw_height, preserveAspectRatio=True)

        # 每两张票后创建新页面
        if position == INVOICES_PER_PAGE - 1 or i == len(invoices) - 1:
            c.showPage()

    c.save()


def main():
    """主函数"""
    print("=" * 60)
    print("火车票发票合并工具")
    print("=" * 60)
    print("开始处理火车票发票...")

    # 检查当前目录是否有ZIP文件
    zip_files = list(Path(".").glob("*.zip"))
    if not zip_files:
        print("\n错误：当前目录没有找到ZIP文件！")
        print("请将包含发票PDF的ZIP文件放在当前目录下。")
        return

    # 1. 解压ZIP文件
    print("\n1. 解压ZIP文件...")
    temp_dir, zip_count = extract_zips(".")

    # 2. 收集并排序发票
    print("\n2. 提取并排序发票信息...")
    invoices = collect_and_sort_invoices(temp_dir)
    print(f"   共找到 {len(invoices)} 张发票")

    if not invoices:
        print("\n错误：未找到任何发票！")
        shutil.rmtree(temp_dir)
        return

    # 显示排序结果
    print("\n发票排序结果（按乘车日期）:")
    print("-" * 70)
    for i, inv in enumerate(invoices, 1):
        date_str = inv['travel_date'].strftime('%Y-%m-%d') if inv['travel_date'] != datetime.min else '未知'
        print(f"   {i:2d}. {date_str} | 车次:{inv['train_no']:6} | 票价:￥{inv['price']:>6}")
    print("-" * 70)

    # 计算总金额
    total = sum(float(inv['price']) if inv['price'] != '未知' else 0 for inv in invoices)
    print(f"\n总金额: ¥{total:.2f}")

    # 3. 生成合并PDF
    print("\n3. 生成合并PDF...")
    if invoices[0]['travel_date'] != datetime.min and invoices[-1]['travel_date'] != datetime.min:
        date_range = f"{invoices[0]['travel_date'].strftime('%Y%m%d')}_to_{invoices[-1]['travel_date'].strftime('%Y%m%d')}"
    else:
        date_range = "按时间排序"
    output_path = f"火车票发票_合并_{date_range}.pdf"

    create_merged_pdf(invoices, output_path)
    print(f"   已生成: {output_path}")

    # 4. 清理临时文件
    print(f"\n4. 清理临时文件...")
    shutil.rmtree(temp_dir)
    print("   清理完成")

    # 计算页数
    total_pages = (len(invoices) + INVOICES_PER_PAGE - 1) // INVOICES_PER_PAGE

    print("\n" + "=" * 60)
    print(f"完成！共处理 {len(invoices)} 张发票，合并为 {total_pages} 页")
    print(f"每页包含 {INVOICES_PER_PAGE} 张发票，按时间顺序排列")
    print("=" * 60)


if __name__ == "__main__":
    main()
