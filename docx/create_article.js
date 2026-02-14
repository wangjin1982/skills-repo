const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat } = require('docx');
const fs = require('fs');

const doc = new Document({
  numbering: {
    config: [
      { reference: "bullet-list", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbered-list", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 56, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 } }
    ]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("电气设计不等于电气画图")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: "——关于电气工程设计本质的思考", italics: true })] }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun('近期，行业内有声音将"Excel 清单自动布置到图纸"这类功能称为"数十年前就已实现的自动化"，并将 PDF 转图纸视为节省重复性劳动的技术突破。作为电气工程设计领域的长期从业者，我们认为有必要澄清一个根本性的问题：')] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: "电气设计，绝不等于电气画图。", bold: true, size: 28 })] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('一、"画图"只是设计的呈现形式，而非设计本身')] }),
      new Paragraph({ spacing: { after: 160 }, children: [new TextRun('将 PDF 转换为图纸，或者将清单自动布置到页面上，这些功能确实可以节省工程师的时间。但我们要清醒地认识到：这些仅仅是')] }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "代替人工绘制线条的工具", bold: true })] }),
      new Paragraph({ children: [new TextRun('，属于"画图"层面的效率提升，而非"设计"层面的本质突破。')] }),
      new Paragraph({ spacing: { before: 160, after: 160 }, children: [new TextRun('电气工程设计的核心价值，从来不是把线条画在纸上，而是：')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "工程计算与选型", bold: true })] }),
      new Paragraph({ indent: { left: 720 }, children: [new TextRun('负载计算、短路电流计算、压降校验、保护配合分析')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "原理验证与优化", bold: true })] }),
      new Paragraph({ indent: { left: 720 }, children: [new TextRun('控制逻辑的正确性、可靠性分析、故障场景模拟')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "标准符合性", bold: true })] }),
      new Paragraph({ indent: { left: 720 }, children: [new TextRun('IEC、NFPA、GB 等国际国内标准的严格遵循')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "跨专业协同", bold: true })] }),
      new Paragraph({ indent: { left: 720 }, children: [new TextRun('与机械、液压、软件、工艺等专业的数据互通')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "全生命周期管理", bold: true })] }),
      new Paragraph({ indent: { left: 720, spacing: { after: 200 } }, children: [new TextRun('从设计、制造、调试到维护的数据一致性')] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun('当一个工具声称能够"一键生成"图纸时，我们必须追问：')] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: '它生成的仅仅是图形，还是经过了工程验证的设计？', bold: true, color: "FF0000" })] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('二、真正的 AI 辅助，是智能辅助设计决策')] }),
      new Paragraph({ spacing: { after: 160 }, children: [new TextRun('我们所倡导的 AI 辅助设计，不是简单地让机器代替人画图，而是让 AI 成为工程师的')] }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "智能助手", bold: true })] }),
      new Paragraph({ children: [new TextRun('，在以下关键环节提供支持：')] }),
      new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [new TextRun({ text: "设计规则检查", bold: true })] }),
      new Paragraph({ indent: { left: 720 }, children: [new TextRun('自动识别违反标准的设计缺陷，如线径过小、保护配合不当等')] }),
      new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [new TextRun({ text: "智能选型建议", bold: true })] }),
      new Paragraph({ indent: { left: 720 }, children: [new TextRun('基于负载特性、工作环境、成本预算，推荐最优元器件组合')] }),
      new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [new TextRun({ text: "设计优化", bold: true })] }),
      new Paragraph({ indent: { left: 720 }, children: [new TextRun('分析同类项目的历史数据，提出能效优化、成本节约的建议')] }),
      new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [new TextRun({ text: "知识沉淀", bold: true })] }),
      new Paragraph({ indent: { left: 720, spacing: { after: 200 } }, children: [new TextRun('将企业多年的设计经验转化为可复用的设计模板和规则库')] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun('这些能力，才是真正提升电气工程设计价值的方向。一个能画图的工具不难做，但一个能"理解"电气原理、辅助工程决策的系统，需要深厚的行业积累。')] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('三、工程数据的完整性，比图纸本身更重要')] }),
      new Paragraph({ spacing: { after: 160 }, children: [new TextRun('在工业4.0和数字化转型的背景下，电气设计的交付物早已不是一堆图纸，而是一套')] }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "完整的数字化工程数据", bold: true })] }),
      new Paragraph({ children: [new TextRun('。这些数据将直接服务于：')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun('PLC 自动化编程')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun('3D 虚拟装配与干涉检查')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun('生产制造执行系统（MES）')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 200 }, children: [new TextRun('数字化运维与远程诊断')] }),
      new Paragraph({ spacing: { after: 160 }, children: [new TextRun('如果 AI 仅仅是"读取 PDF 并生成图纸"，那么生成的图纸中是否包含：')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun('完整的设备属性数据？')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun('标准化的器件标识体系？')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 200 }, children: [new TextRun('可被下游系统直接调用的结构化数据？')] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun('没有这些，生成的图纸不过是一张"漂亮的图片"，无法支撑数字化工厂的运行。')] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('四、工程师的价值，在于对设计结果的负责')] }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun('无论是 AI 辅助还是自动化工具，最终对设计安全性、可靠性负责的，始终是')] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: "持证的电气工程师", bold: true })] }),
      new Paragraph({ children: [new TextRun('。这意味着：')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun('工具可以辅助画图，但不能替代工程师对设计原则的判断')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun('工具可以提供计算结果，但不能替代工程师对边界条件的理解')] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 200 }, children: [new TextRun('工具可以生成选项，但不能替代工程师对权衡决策的担当')] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun('我们欢迎任何能够提升工程师效率的技术，但技术的终点，应该是让工程师有更多精力专注于"真正的设计工作"——那些需要专业经验、工程判断和创新思维的环节，而不是让他们从一个"画图员"变成一个"图纸审核员"。')] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('五、结语')] }),
      new Paragraph({ spacing: { after: 160 }, children: [new TextRun('电气工程设计是一门严谨的工程学科，承载着安全、可靠、高效的工业使命。我们始终相信，技术的进步应该让工程师的工作')] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: "更有价值、更有尊严、更有创造性", bold: true })] }),
      new Paragraph({ children: [new TextRun('。')] }),
      new Paragraph({ spacing: { before: 160, after: 160 }, children: [new TextRun('如果一项技术的亮点在于"把工程师从画线中解放出来"，那我们不妨追问：解放出来之后，工程师应该去做什么？如果答案是"去审核 AI 画的图纸是否有问题"，那我们不过是把重复性劳动变成了重复性审核。')] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: '真正的进步，是让工程师从"画图"升级到"设计"，从"绘图员"升级到"工程师"。', bold: true })] }),
      new Paragraph({ children: [new TextRun('这才是我们对电气设计未来的期许。')] }),
      new Paragraph({ pageBreakBefore: true, spacing: { before: 240, after: 160 }, children: [new TextRun({ text: "——", bold: true })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "EPLAN 致力于为电气工程设计提供完整的数字化解决方案，", bold: true })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "让工程师的每一份投入，都产生真正的工程价值。", bold: true })] }]
    }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(process.env.HOME + "/Documents/电气设计不等于电气画图.docx", buffer);
  console.log("Word 文档已创建");
});
