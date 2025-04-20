from zmprinter import LabelPrinterSDK, PrinterConfig, LabelConfig, PrinterStyle

# 初始化打印机配置
printer_config = PrinterConfig(
    interface=PrinterStyle.USB,
    dpi=300,
    speed=4,
    darkness=10,
)

# 初始化标签配置
label_config = LabelConfig(
    width=60.0,
    height=40.0,
)

# 创建SDK实例
printer = LabelPrinterSDK(printer_config=printer_config, label_config=label_config)

# 读取LSF文件
printer_config, label_config, elements, status = printer.read_lsf("example.lsf")

if status:
    print(f"读取LSF文件失败: {status}")
elif not elements:
    print("标签元素为空")
else:
    print(f"打印机配置: {printer_config}")
    print(f"标签配置: {label_config}")
    print(f"标签元素数量: {len(elements)}")

    # 打印标签
    result, count = printer.print_label(elements)
    print(f"打印结果: {result}, 打印数量: {count}")
