from zmprinter import LabelPrinterSDK, PrinterConfig, LabelConfig, PrinterStyle

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

# 读取UHF RFID标签数据
tag_data = printer.read_uhf_tag(
    area=0,  # 0: TID, 1: EPC, 2: TID+EPC
    power=0,  # 读取功率 (0表示使用打印机当前设置)
    stop_position=2,  # 读取后标签停止位置 (2:打印位置)
    timeout=2000,  # 超时时间 (毫秒)
)

print(f"读取到的RFID标签数据: {tag_data}")
