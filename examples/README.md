# ZMPrinter SDK 示例

本目录包含了一系列使用 `zmprinter` SDK 的示例代码，帮助您快速上手打印机操作。

## 示例列表

1. **basic_usage.py** - 基本用法示例，打印一个包含文本和条码的标签。
2. **rfid_printing.py** - 打印并写入RFID标签的示例。
3. **label_preview.py** - 生成标签预览图像的示例。
4. **read_rfid.py** - 读取RFID标签数据的示例。
5. **read_lsf.py** - 读取LSF标签文件并打印的示例。
6. **read_lsf_file.py** - 读取LSF文件并解析其内容的示例。
7. **print_barcode.py** - 生成条码标签并打印或预览的示例。
8. **simple_preview.py** - 生成简单文本标签预览的示例。

## 运行示例

确保您已安装 `zmprinter` SDK 和所需的依赖项。然后，可以直接运行示例脚本：

```bash
python examples/basic_usage.py
```

## 注意事项

- 确保打印机已正确连接并配置。
- 对于RFID相关示例，确保打印机支持RFID功能。
- 对于LSF文件示例，确保 `example.lsf` 文件存在。
- 部分示例支持命令行参数，可通过 `--help` 查看详细用法。