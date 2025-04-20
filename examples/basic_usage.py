from zmprinter import LabelPrinterSDK, PrinterConfig, LabelConfig, TextElement, BarcodeElement, PrinterStyle

# 初始化打印机配置
printer_config = PrinterConfig(
    interface=PrinterStyle.USB,  # 使用USB接口
    dpi=300,  # 打印分辨率
    speed=4,  # 打印速度
    darkness=10,  # 打印浓度
)

# 初始化标签配置
label_config = LabelConfig(
    width=60.0,  # 标签宽度，单位mm
    height=40.0,  # 标签高度，单位mm
)

# 创建SDK实例
printer = LabelPrinterSDK(printer_config=printer_config, label_config=label_config)

# 创建文本元素
text_element = TextElement(
    object_name="text-01",
    data="Hello, World!",
    x=10.0,  # 水平位置
    y=10.0,  # 垂直位置
    font_name="黑体",
    font_size=12.0,
)

# 创建条码元素
barcode_element = BarcodeElement(
    object_name="barcode-01",
    data="123456789",
    barcode_type="Code 128 Auto",
    x=10.0,
    y=20.0,
    scale=3.0,
)

# 打印标签
result, count = printer.print_label([text_element, barcode_element])
print(f"打印结果: {result}, 打印数量: {count}")
