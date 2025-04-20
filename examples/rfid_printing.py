from zmprinter import LabelPrinterSDK, PrinterConfig, LabelConfig, TextElement, RFIDElement, PrinterStyle
from zmprinter.enums import RFIDEncoderType, RFIDDataBlock, RFIDDataType

# 初始化打印机配置 (使用RFID接口)
printer_config = PrinterConfig(
    interface=PrinterStyle.RFID_USB,  # 使用RFID_USB接口
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
    data="RFID Label",
    x=10.0,
    y=10.0,
    font_name="黑体",
    font_size=12.0,
)

# 创建RFID元素
rfid_element = RFIDElement(
    object_name="rfiduhf-01",
    data="EPC123456789",  # 要写入的RFID数据
    rfid_encoder_type=RFIDEncoderType.UHF,  # UHF RFID
    rfid_data_block=RFIDDataBlock.EPC,  # 写入EPC区
    rfid_data_type=RFIDDataType.HEX,  # 16进制数据
)

# 打印标签 (同时写入RFID)
result, count = printer.print_label([text_element, rfid_element])
print(f"打印结果: {result}, 打印数量: {count}")
