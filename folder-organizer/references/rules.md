# Classification Rules

## Target Structure

- `01_客户与项目/`
- `02_产品与技术/`
- `03_培训与课程/`
- `04_销售与咨询/`
- `05_运营与行政/`
- `06_素材与多媒体/`
- `00_收件箱_待分类/`
- `个人学习/`

## Rule Priority

1. Explicit extension rules (e.g. media, executable)
2. Filename/path keyword rules
3. Default fallback to `00_收件箱_待分类/`

## Extension Rules

- Media -> `06_素材与多媒体/`: `jpg,jpeg,png,bmp,gif,webp,mp4,mov,mkv,wmv,avi,flv,html,htm`
- Executable/unknown binary -> `00_收件箱_待分类/`: `exe,dmg,pkg,wrf`
- Engineering package -> `01_客户与项目/`: `hxzproj`

## Keyword Rules

### `01_客户与项目/`
`项目,客户,实施,交付,需求,接口,SOW,周报,POC,集成`

### `02_产品与技术/`
`产品,技术,测试,手册,API,端口,viewer`

### `03_培训与课程/`
`培训,研讨会,考试,题库,教育,课程,讲义,笔记`

### `04_销售与咨询/`
`售前,咨询,商机,竞品,competitor,kick off,qbr,rebranding,建议`

### `05_运营与行政/`
`行政,运营,kpi,发票,报销,会议,借贷,license,合同流程`

### `个人学习/`
`学习,数据之道,读书,课程笔记`
