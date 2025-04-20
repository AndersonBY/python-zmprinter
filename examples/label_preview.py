from zmprinter import LabelPrinterSDK, PrinterConfig, LabelConfig, TextElement, BarcodeElement, PrinterStyle


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

# 创建文本元素
text_element = TextElement(
    object_name="text-01",
    data="Preview Label",
    x=10.0,
    y=10.0,
    font_name="黑体",
    font_size=12.0,
)

# 创建条码元素
barcode_element = BarcodeElement(
    object_name="barcode-01",
    data="987654321",
    barcode_type="Code 128 Auto",
    x=10.0,
    y=20.0,
    scale=3.0,
)

# 生成标签预览
preview_image = printer.preview_label([text_element, barcode_element])

if preview_image:
    # 显示预览图像
    preview_image.show()

    # 保存预览图像
    preview_image.save("label_preview.png")
    print("标签预览已保存为 'label_preview.png'")
else:
    print("标签预览失败")
