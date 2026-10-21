# 环境要求

阅读 Markdown、查看图表和 CSV 文件不需要安装 Python。

仓库维护脚本使用 Python 3.10 及以上版本的标准库，无第三方依赖。可在项目根目录运行：

```sh
python scripts/check_repository.py
python scripts/export_book.py
```

第一个脚本检查目录、内部链接、图片、引用编号和表格文件。第二个脚本根据 `book.json` 中的顺序生成根目录的 `book.md`。

[返回首页](README.md)
