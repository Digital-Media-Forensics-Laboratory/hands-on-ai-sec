# 动手学人工智能安全

围绕开源大模型的内容安全，学习模型发展、风险识别、安全评价、开源社区治理与规范管理。

[开始阅读](chapter_introduction/index.md) · [完整目录](index.md) · [全文阅读](book.md) · [参考文献](chapter_references/index.md)

## 章节

| 章 | 内容 | 节数 |
| --- | --- | --- |
| 1 | [绪论](chapter_introduction/index.md) | 4 |
| 2 | [开源大模型发展现状与内容安全风险概述](chapter_development-and-risks/index.md) | 3 |
| 3 | [国内外开源大模型内容安全治理方法与实践](chapter_research-progress/index.md) | 3 |
| 4 | [开源大模型内容安全风险识别与态势分析](chapter_risk-identification/index.md) | 4 |
| 5 | [开源大模型内容安全评估指标体系构建](chapter_evaluation-framework/index.md) | 5 |
| 6 | [开源社区管理与开源生态发展](chapter_open-source-governance/index.md) | 4 |
| 7 | [内容安全规范管理策略与政策建议](chapter_management-strategies/index.md) | 6 |

## 阅读与使用

各章目录位于仓库根目录的 `chapter_*` 文件夹中。章内按小节拆分 Markdown，页面提供本章目录、全书目录及上一节、下一节导航。图表随正文排布，表格另有 [CSV 文件](data/README.md)，便于查阅。

本版共七章、29 节，大模型安全评测系统等实操章节将在后续加入。

在 GitHub 或本地 Markdown 阅读器中阅读即可。运行仓库检查、重新生成全文阅读文件，需要 Python 3.10 或以上版本，无需安装第三方依赖。

```sh
python scripts/check_repository.py
python scripts/export_book.py
```

## 仓库文件

- [目录](index.md)
- [表格数据](data/README.md)
- [环境要求](ENVIRONMENT.md)
- [贡献说明](CONTRIBUTING.md)
- [发布说明](PUBLISHING.md)
- [许可说明](LICENSE)

版本：v0.3.3。

## 许可说明

除另有说明外，本项目的原创内容采用 [Apache License 2.0](LICENSE) 发布。

引用的第三方图表、模型、代码及其他材料，仍遵循各自的许可和使用条件。
