---
name: eplan-research-report
description: Generate Eplan Digital Consulting Research Reports as formatted Word documents (.docx). Use when user says "生成 Eplan 调研报告" or "generate Eplan research report" or needs to create a structured consulting report with customer analysis, pain points, data flow analysis, ROI assumptions, and implementation roadmap. Collects client name and key pain points from user, then generates complete professional report with cover page and all standard sections.
---

# Eplan Research Report Generator

Generate professional Eplan Digital Consulting research reports as formatted Word documents.

## Workflow

### 1. Collect Required Information

Ask the user for:
- **Client name** (客户名称) - Required
- **Key pain points** (关键痛点) - Required, user provides specific pain points
- **Report date** (报告日期) - Optional, defaults to current YYYY年MM月

Example prompt:
```
请提供以下信息来生成调研报告：
1. 客户公司名称
2. 关键业务痛点（已发现的主要问题）
3. 报告日期（可选，默认为当前月份）
```

### 2. Generate Report Using Script

Use the provided Python script to generate the report:

```bash
python /path/to/skill/scripts/generate_report.py \
  "<client_name>" \
  "<output_path>/<client_name>_调研报告.docx" \
  "<report_date>"
```

### 3. Fill Report Content

After generating the template, use docx skill to populate each section:

#### Section 1: Customer Current State Analysis (客户现状分析)
- Company background and industry context
- Current engineering tools and processes
- Organization structure
- Existing capabilities and limitations

#### Section 2: Business Pain Points (业务痛点)
Use the pain points provided by the user, expand with:
- Impact on operations
- Root causes where identifiable
- Affected departments/stakeholders

#### Section 3: Data Flow Analysis (数据流分析)
Based on the customer's domain and pain points:
- Current data sources and destinations
- Process workflow visualization
- Integration points and hand-offs
- Bottlenecks in current flow

#### Section 4: ROI Assumptions (ROI 假设)

##### 4.1 Investment Cost Analysis
List typical costs:
- Eplan software licensing
- Implementation services
- Training and change management
- Infrastructure requirements
- Ongoing support costs

##### 4.2 Expected Benefits Analysis
Quantify benefits:
- Time savings per user (hours/year)
- Error reduction (%)
- Rework reduction
- Standardization benefits

##### 4.3 Quantitative Metrics
Provide specific metrics:
- Efficiency improvement: X%
- Annual cost savings: ¥XXX,XXX
- Quality improvement: X%
- Payback period: X months

##### 4.4 Investment Payback Period
Calculate and explain:
- Total investment vs. annual savings
- Payback period in months/years
- Sensitivity considerations

#### Section 5: Implementation Roadmap (实施路径)
Propose phased approach:
- Phase 1: Planning & Preparation
- Phase 2: Pilot implementation
- Phase 3: Full rollout
- Phase 4: Training & adoption
- Phase 5: Continuous improvement

### 4. Review and Deliver

- Verify all sections are complete
- Check calculations in ROI section
- Ensure professional tone throughout
- Confirm formatting is consistent
- Provide file location to user

## Report Structure Reference

See [report_structure.md](references/report_structure.md) for detailed content guidance on each section including:
- What information to include
- How to structure analysis
- Common pain points to address
- ROI calculation framework
- Writing guidelines and tone

## Script Capabilities

The `generate_report.py` script provides:
- Professional cover page with client name and date
- Pre-formatted section headers (1-5)
- Subsection structure for ROI analysis
- Consistent typography and spacing
- A4 page layout with 1-inch margins
- Microsoft YaHei font for Chinese text

## Dependencies

- python-docx: `pip install python-docx`

## Output Format

- File type: .docx (Word document)
- Page size: A4
- Margins: 1 inch on all sides
- Font: Microsoft YaHei (primary), sizing by section
- Colors: Professional blue (#003366) for headings
