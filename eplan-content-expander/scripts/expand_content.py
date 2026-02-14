#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPLAN 内容扩写脚本
根据客户信息生成详细的业务范围、产品线和企业背景内容
"""

import os
import sys
from typing import Dict, List

class ContentExpander:
    """EPLAN 报告内容扩写器"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """加载扩写模板"""
        return {
            # 业务范围模板
            "business_scope": {
                "rd": self._rd_template(),
                "production": self._production_template(),
                "technical_service": self._technical_service_template(),
                "system_integration": self._system_integration_template(),
            },
            # 产品线模板
            "product_lines": {
                "hv_cabinet": self._hv_cabinet_template(),
                "lv_cabinet": self._lv_cabinet_template(),
                "distribution_box": self._distribution_box_template(),
                "busbar_bridge": self._busbar_bridge_template(),
            },
            # 企业背景模板
            "company_background": {
                "introduction": self._company_introduction_template(),
                "history": self._history_template(),
                "organization": self._organization_template(),
            },
        }

    def expand_section(self, section_type: str, client_name: str, **kwargs) -> str:
        """扩写指定章节的内容

        section_map = {
            "business_scope": {
                "rd": kwargs.get("rd_focus", []),
                "production": kwargs.get("production_focus", []),
                "technical_service": kwargs.get("service_focus", []),
                "system_integration": kwargs.get("integration_focus", []),
            },
            "product_lines": kwargs.get("product_details", {}),
            "company_background": kwargs.get("company_info", {}),
        }

        if section_type not in section_map:
            return f"# 错误：未知的章节类型 '{section_type}'"

        template = self.templates.get(section_type)
        if not template:
            return f"# 错误：章节 '{section_type}' 没有模板"

        # 扩写内容
        if section_type == "business_scope":
            content = self._expand_business_scope(client_name, **kwargs)
        elif section_type == "product_lines":
            content = self._expand_product_lines(client_name, **kwargs)
        elif section_type == "company_background":
            content = self._expand_company_background(client_name, **kwargs)
        else:
            content = template

        return f"## {kwargs.get('title', section_type.replace('_', ' ').title())}\n\n{content}"

    def _rd_template(self) -> str:
        """科研开发模板"""
        return """江苏海航电气科技有限公司始终将技术创新作为企业发展的核心驱动力。

公司组建了专业的研发团队，专注于高低压电器成套设备的前沿技术研究与产品开发。研发方向涵盖智能化配电技术、电能质量优化、环保型开关设备等多个新兴领域。通过与国内知名高校和科研院所的深度合作，公司不断将最新技术成果转化为实际生产力。

截至目前，公司已获得多项发明和实用新型专利，形成了具有自主知识产权的核心技术体系。特别是在智能电网、新能源接入、工业自动化控制等新兴领域，公司持续加大研发投入，确保产品技术始终处于行业领先水平。"""

    def _production_template(self) -> str:
        """生产经营模板"""
        return """公司建立了现代化的生产制造基地，配备了先进的生产设备和检测仪器。

生产车间采用精益化管理模式，严格执行 ISO9001 质量管理体系标准，确保每道工序都符合规范要求。生产线涵盖从钣金加工、表面处理、装配调试到成品检验的全流程，具备年产高低压开关柜数千台、各类配电箱数万台的规模化生产能力。

产品覆盖高压（12kV-40.5kV）、中压（3.6kV-6kV）、低压（380V/660V）全系列电压等级，能够满足不同行业、不同场景的应用需求。公司还建立了完善的供应链管理体系，与国内外知名元器件厂商建立了长期稳定的合作关系，从源头上保证产品质量。"""

    def _technical_service_template(self) -> str:
        """技术服务模板"""
        return """江苏海航不仅提供优质的产品，更注重为客户提供全方位的技术服务。

服务团队由经验丰富的工程师组成，可为客户提供从项目初期的方案设计、产品选型到安装调试、运维支持的全生命周期技术服务。对于复杂项目，公司能够提供系统集成服务，将配电系统、控制系统、自动化系统等多个子系统进行优化整合。

从方案论证、系统设计到设备成套、现场安装、联调测试，公司提供一站式服务，确保各子系统无缝衔接、协同工作。近年来，公司已成功为钢铁冶金、石油化工、轨道交通、数据中心等多个行业的大型项目提供了系统集成服务，积累了丰富的项目经验。"""

    def _system_integration_template(self) -> str:
        """系统集成模板"""
        return """针对不同行业客户的特殊需求，江苏海航提供系统集成服务，将配电系统、控制系统、自动化系统等多个子系统进行优化整合。

公司拥有强大的系统设计能力和项目实施经验，能够根据客户的工艺特点、场地条件、预算规模等因素，量身定制最优的电气系统解决方案。从方案论证、系统设计到设备成套、现场安装、联调测试，公司提供一站式服务，确保各子系统无缝衔接、协同工作。

公司熟悉主流的 PLC 品牌（如西门子、施耐德、三菱、欧姆龙等）和人机界面（HMI）设计软件，能够与客户的 MES 系统、ERP 系统实现数据对接。在自动化控制方面，公司拥有丰富的项目经验，涵盖从简单的继电器逻辑控制到复杂的 PLC+触摸屏+伺服系统集成的各类应用。"""

    def _hv_cabinet_template(self) -> str:
        """高压开关柜模板"""
        return """| 系列 | 型号 | 额定电压 | 额定电流 | 防护等级 | 应用场景 |
|-----|------|---------|---------|---------|
| KYN28 | 12kV | 630A | IP40 | 变电站、发电厂 |
| XGN15 | 12kV | 630A | IP40 | 工矿企业供电 |

**产品特点说明**：
- 采用先进的灭弧技术，确保操作安全
- 柜体采用敷铝锌板，耐腐蚀能力强
- 内部采用高品质的绝缘件，电气寿命长
- 符合 GB 3906、IEC 60298 等国际标准
- 通过了型式试验和运行验证，质量可靠"""

    def _lv_cabinet_template(self) -> str:
        """低压开关柜模板"""
        return """| 系列 | 型号示例 | 额定电压 | 额定电流 | 功能特点 |
|-----|---------|---------|---------|---------|
| GCS | GCS-450 | 380V | 630A-630A | 固定式、抽出式 |

**产品特点说明**：
- 可选配智能控制器（西门子、施耐德等）
- 支持多种操作模式（手动、自动）
- 具备通讯接口，可接入上位机系统
- 适用于各类工业厂房、商业建筑、基础设施"""

    def _company_introduction_template(self) -> str:
        """公司简介模板"""
        return """江苏海航电气科技有限公司成立于 **2003年**，是一家拥有二十余年行业经验的高新技术企业。

公司坐落于中国江苏省，地处长三角经济圈，享有得天独厚的产业配套优势和地理区位优势。作为电气成套设备领域的专业制造商，江苏海航电气科技有限公司始终专注于为客户提供高品质的产品和全方位的技术服务。公司凭借深厚的技术积累、严格的质量管理体系和持续创新的能力，在行业内建立了良好的声誉和品牌影响力。"""

    def _history_template(self) -> str:
        """发展历程模板"""
        return """自成立以来，江苏海航电气科技有限公司经历了多个重要的发展阶段：

**初创期（2003-2010年）**：公司成立并建立基础生产线，完成首批产品认证，进入电气成套设备市场。

**成长期（2011-2015年）**：扩大生产规模，引入先进生产设备，建立质量管理体系，产品线日趋完善。

**扩张期（2016-2020年）**：拓展业务范围，增加系统集成服务，进入新能源、轨道交通等新领域。

**成熟期（2021年至今）**：持续技术创新，获得高新技术企业认定，建立研发中心，提升品牌影响力。"""

    def _organization_template(self) -> str:
        """组织架构模板"""
        return """公司采用现代化的企业管理模式，设有完善的组织架构：

**研发中心**：负责新产品研发、技术改进、专利申请
**生产制造部**：下设多个车间，负责生产制造、质量检验、设备维护
**技术支持部**：提供售前技术支持、项目实施、售后运维服务
**市场部**：负责市场开拓、销售管理、客户关系维护

公司注重人才培养，建立了科学的薪酬体系和晋升通道，确保团队的稳定性和持续发展。"""

    def _expand_business_scope(self, client_name: str,
                          rd_focus: List[str] = None,
                          production_focus: List[str] = None,
                          service_focus: List[str] = None,
                          integration_focus: List[str] = None) -> str:
        """扩写业务范围内容"""
        parts = []

        if rd_focus:
            parts.append(self._expand_rd(client_name, rd_focus))
        if production_focus:
            parts.append(self._expand_production(client_name, production_focus))
        if service_focus:
            parts.append(self._expand_technical_service(client_name, service_focus))
        if integration_focus:
            parts.append(self._expand_system_integration(client_name, integration_focus))

        return "\n\n".join(parts)

    def _expand_rd(self, client_name: str, focus: List[str]) -> str:
        """扩写科研开发"""
        focus_text = "、".join(f"**{f}**" for f in focus)
        return f"""
**1. 科研开发**

{client_name}{focus_text}

公司组建了专业的研发团队，专注于高低压电器成套设备的前沿技术研究与产品开发。研发方向涵盖智能化配电技术、电能质量优化、环保型开关设备等多个新兴领域。通过与国内知名高校和科研院所的深度合作，公司不断将最新技术成果转化为实际生产力。
"""

    def _expand_production(self, client_name: str, focus: List[str]) -> str:
        """扩写生产经营"""
        focus_text = "、".join(f"**{f}**" for f in focus)
        return f"""
**2. 生产经营**

{client_name}{focus_text}

公司建立了现代化的生产制造基地，配备了先进的生产设备和检测仪器。生产车间采用精益化管理模式，严格执行 ISO9001 质量管理体系标准，确保每道工序都符合规范要求。生产线涵盖从钣金加工、表面处理、装配调试到成品检验的全流程，具备年产高低压开关柜数千台、各类配电箱数万台的规模化生产能力。

产品覆盖高压（12kV-40.5kV）、中压（3.6kV-6kV）、低压（380V/660V）全系列电压等级，能够满足不同行业、不同场景的应用需求。公司还建立了完善的供应链管理体系，与国内外知名元器件厂商建立了长期稳定的合作关系，从源头上保证产品质量。"""

    def _expand_technical_service(self, client_name: str, focus: List[str]) -> str:
        """扩写技术服务"""
        focus_text = "、".join(f"**{f}**" for f in focus)
        return f"""
**3. 技术服务**

{client_name}{focus_text}

江苏海航不仅提供优质的产品，更注重为客户提供全方位的技术服务。服务团队由经验丰富的工程师组成，可为客户提供从项目初期的方案设计、产品选型到安装调试、运维支持的全生命周期技术服务。对于复杂项目，公司能够提供系统集成服务，将配电系统、控制系统、自动化系统等多个子系统进行优化整合。

从方案论证、系统设计到设备成套、现场安装、联调测试，公司提供一站式服务，确保各子系统无缝衔接、协同工作。近年来，公司已成功为钢铁冶金、石油化工、轨道交通、数据中心等多个行业的大型项目提供了系统集成服务，积累了丰富的项目经验。"""

    def _expand_system_integration(self, client_name: str, focus: List[str]) -> str:
        """扩写系统集成"""
        focus_text = "、".join(f"**{f}**" for f in focus)
        return f"""
**4. 系统集成**

{client_name}{focus_text}

针对不同行业客户的特殊需求，江苏海航提供系统集成服务，将配电系统、控制系统、自动化系统等多个子系统进行优化整合。

公司拥有强大的系统设计能力和项目实施经验，能够根据客户的工艺特点、场地条件、预算规模等因素，量身定制最优的电气系统解决方案。从方案论证、系统设计到设备成套、现场安装、联调测试，公司提供一站式服务，确保各子系统无缝衔接、协同工作。

公司熟悉主流的 PLC 品牌（如西门子、施耐德、三菱、欧姆龙等）和人机界面（HMI）设计软件，能够与客户的 MES 系统、ERP 系统实现数据对接。在自动化控制方面，公司拥有丰富的项目经验，涵盖从简单的继电器逻辑控制到复杂的 PLC+触摸屏+伺服系统集成的各类应用。"""

    def _expand_product_lines(self, client_name: str, product_details: Dict) -> str:
        """扩写产品线内容"""
        if not product_details:
            return ""

        parts = []
        for category, details in product_details.items():
            if isinstance(details, dict) and details:
                parts.append(f"""
#### {category.replace('_', ' ').title()}

| 系列 | 型号 | 额定电压 | 额定电流 | 防护等级 | 应用场景 |
|-----|------|---------|---------|---------|
""")

                # 添加表格内容
                if "models" in details:
                    for model in details["models"]:
                        parts.append(f"| {model.get('name', model.get('型号', '-')) | {model.get('电压', '-')} | {model.get('current', '-')} | {model.get('protection', '-')} | {model.get('application', '-')} |")
                    parts.append("| :---:|---------|---------|---------|---------|")

                # 添加特点说明
                if "features" in details:
                    features = details["features"]
                    parts.append(f"""
**产品特点说明**：
""")
                    for feature in features:
                        parts.append(f"- {feature}")
                    parts.append("\n")
                # 添加说明
                if "description" in details:
                    parts.append(f"{details['description']}")

        return "\n\n".join(parts)

    def _expand_company_background(self, client_name: str, company_info: Dict) -> str:
        """扩写企业背景内容"""
        parts = []

        if "introduction" in company_info:
            parts.append(f"""
### 1.1 企业背景

{company_info['introduction']}
""")

        if "history" in company_info:
            parts.append(f"""
### 1.2 发展历程

{company_info['history']}
""")

        if "organization" in company_info:
            parts.append(f"""
### 1.3 组织架构

{company_info['organization']}
""")

        return "\n\n".join(parts)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='EPLAN 内容扩写工具')
    parser.add_argument('--client', type=str, help='客户名称')
    parser.add_argument('--section', type=str, choices=['business_scope', 'product_lines', 'company_background'],
                       help='要扩写的章节')
    parser.add_argument('--preview', action='store_true', help='预览扩写效果')

    # 业务范围相关参数
    parser.add_argument('--rd-focus', nargs='+', type=str, help='科研开发重点（如：研发团队 技术方向）')
    parser.add_argument('--production-focus', nargs='+', type=str, help='生产经营重点（如：生产线 产能规模）')
    parser.add_argument('--service-focus', nargs='+', type=str, help='技术服务重点（如：服务范围 项目实施）')
    parser.add_argument('--integration-focus', nargs='+', type=str, help='系统集成重点（如：定制化能力 行业案例）')

    # 产品线参数
    parser.add_argument('--product-details', type=str, help='产品线详情（JSON 格式）')

    # 企业背景参数
    parser.add_argument('--company-info', type=str, help='企业背景详情（JSON 格式）')

    args = parser.parse_args()

    expander = ContentExpander()

    if args.preview:
        # 预览模式：展示扩写效果
        if args.section == 'business_scope':
            print(f"## 业务范围扩写预览（目标：~500 字）")
            print(expander._expand_business_scope(args.client,
                rd_focus=args.rd_focus or ["研发团队", "技术方向", "专利成果", "合作院校"],
                production_focus=args.production_focus or ["生产线", "产能规模", "质量体系", "供应链"],
                service_focus=args.service_focus or ["服务范围", "技术支持", "项目实施"],
                integration_focus=args.integration_focus or ["定制化能力", "行业案例", "技术栈"]))
        elif args.section == 'product_lines':
            print(f"## 产品线扩写预览（目标：~500 字）")
            # 示例产品线
            sample_products = {
                "hv_cabinet": {
                    "models": [
                        {"name": "KYN", "型号": "KYN28", "voltage": "12kV", "current": "630A", "protection": "IP40", "application": "变电站、发电厂"},
                        {"name": "XGN", "型号": "XGN15", "voltage": "12kV", "current": "630A", "protection": "IP40", "application": "工矿企业供电"},
                    ],
                    "features": ["采用先进的灭弧技术，确保操作安全", "采用敷铝锌板，耐腐蚀能力强"],
                    "description": "高压开关柜适用于 12kV-40.5kV 电力系统，采用先进的灭弧技术确保操作安全。柜体采用敷铝锌板，具有良好的耐腐蚀性能。"
                },
                "lv_cabinet": {
                    "models": [{"name": "GCS", "型号": "GCS-450", "voltage": "380V", "current": "630A-630A"}],
                    "features": ["可配智能控制器（西门子、施耐德等）", "支持多种操作模式（手动、自动）", "具通讯接口，可接入上位机系统"],
                }
            }
            print(expander._expand_product_lines(args.client, sample_products))
        elif args.section == 'company_background':
            print(f"## 企业背景扩写预览（目标：~500 字）")
            sample_info = {
                "introduction": "江苏海航电气科技有限公司成立于**2003年**，是一家拥有二十余年行业经验的高新技术企业。",
                "history": "自成立以来，江苏海航经历了初创期（2003-2010年）、成长期（2011-2015年）、扩张期（2016-2020年）和成熟期（2021年至今）四个重要的发展阶段。",
                "organization": "公司采用现代化的企业管理模式，设有完善的组织架构，包括研发中心、生产制造部、技术支持部、市场部等核心部门。"
            }
            print(expander._expand_company_background(args.client, sample_info))
    else:
        print("请指定要预览的章节类型：")
        print("  --section business_scope  预览业务范围扩写")
        print("  --section product_lines 预览产品线扩写")
        print("  --section company_background 预览企业背景扩写")
    else:
        print("\n💡 使用示例：")
        print("python scripts/expand_content.py --client 江苏海航 --section business_scope --preview")
        print("python scripts/expand_content.py --client 江苏海航 --section product_lines --preview")
        print("python scripts/expand_content.py --client 江苏海航 --section company_background --preview")


if __name__ == "__main__":
    main()
