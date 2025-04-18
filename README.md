# ZMPrinter Python SDK

[![PyPI version](https://badge.fury.io/py/zmprinter.svg)](https://badge.fury.io/py/zmprinter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

本 SDK 是对 `LabelPrinter.dll` (适用于 ZM 系列标签打印机) 的 Python 封装，旨在提供一个简洁易用的 Python 接口来控制 ZMPrinter 打印机进行标签设计、预览和打印，包括 RFID 标签的读写操作。

## 主要特性

*   **跨接口支持:** 支持 USB、网络(NET)、驱动(DRIVER) 等多种连接方式，包括对应的 RFID 模式。
*   **标签设计:** 支持文本、条码/二维码、图片、图形（直线、矩形）以及 RFID 写入等多种标签元素。
*   **打印预览:** 可在不实际打印的情况下生成标签预览图 (Pillow Image 对象)。
*   **LSF 文件支持:** 读取 `.lsf` 标签设计文件，解析其中的打印机设置、标签设置和元素，并支持更新变量数据。
*   **RFID 操作:** 支持 UHF (超高频) 和 HF (高频) RFID 标签的读取 (TID, EPC, User data) 和写入 (通过打印)。
*   **打印机状态:** 获取打印机的实时状态 (如：正常、缺纸、开盖、RFID错误等)。
*   **USB 设备发现:** 获取连接到计算机的 USB 打印机主板序列号 (MBSN)。
*   **自动 DLL 加载:** 自动检测操作系统架构 (x86/x64) 并加载相应的 `LabelPrinter.dll`。
*   **配置灵活:** 通过 `PrinterConfig` 和 `LabelConfig` 对象进行详细的打印机和标签参数设置。
*   **日志记录:** 内建日志系统，可通过环境变量配置日志级别和格式。
*   **异常处理:** 定义了详细的异常类，方便捕获和处理 SDK 操作中可能出现的错误。

## 系统要求与依赖

*   **操作系统:** **Windows** (因为依赖 .NET Framework 和底层 USB/驱动交互)。
*   **Python 版本:** >= 3.11
*   **依赖库:**
    *   `pythonnet` (>=3.0.5): 用于 Python 与 .NET DLL 的交互。
    *   `Pillow` (>=11.2.1): 用于处理标签预览图像。
*   **.NET Framework:** 需要安装与 `LabelPrinter.dll` 兼容的 .NET Framework 版本 (根据 DLL 的 `Readme.txt`，其基于 **.NET Framework 2.0** 构建，请确保系统安装了此版本或更高版本)。

## 安装

```bash
pip install zmprinter
```

## 快速开始

以下是一个简单的示例，演示如何连接 USB 打印机、设计标签、预览并打印：

```python
import sys
from pathlib import Path

from zmprinter import (
    LabelPrinterSDK,
    PrinterConfig,
    LabelConfig,
    PrinterStyle,
    BarcodeType,
    TextElement,
    BarcodeElement,
    ImageElement,
    ZMPrinterStateError,
    ZMPrinterCommandError,
    logger # 使用内置 logger
)

try:
    # 1. 配置打印机 (USB 接口, 300 DPI)
    printer_cfg = PrinterConfig(
        interface=PrinterStyle.USB,
        dpi=300,
        speed=4,        # 打印速度 (通常 1-6)
        darkness=10,    # 打印浓度 (通常 0-20)
        has_gap=True    # 标签纸是否有间隙
        # 如果有多台 USB 打印机，可能需要指定 mbsn
        # sn_list = sdk.get_usb_printer_sn()
        # if sn_list:
        #     printer_cfg.mbsn = sn_list[0] # 使用找到的第一个打印机SN
    )
    logger.info(f"打印机配置: 接口={printer_cfg.interface.name}, DPI={printer_cfg.dpi}")

    # 2. 配置标签 (60mm x 40mm, 间隙 2mm)
    label_cfg = LabelConfig(width=60, height=40, gap=2)
    logger.info(f"标签配置: 宽度={label_cfg.width}mm, 高度={label_cfg.height}mm")

    # 3. 初始化 SDK
    # SDK 会尝试自动查找 libs 目录下的 DLL
    # 如果 DLL 在其他位置，可以指定路径: sdk = LabelPrinterSDK(dll_path="C:\\path\\to\\LabelPrinter.dll")
    logger.info("初始化 ZMPrinter SDK...")
    sdk = LabelPrinterSDK(printer_config=printer_cfg, label_config=label_cfg)
    logger.info("SDK 初始化成功.")

    # 4. 创建标签元素列表
    elements = [
        TextElement(
            object_name="text-title", # 元素唯一标识名
            data="欢迎使用 ZMPrinter",
            x=5, y=5,
            font_name="黑体",
            font_size=12,
            font_style=1 # 0:常规, 1:粗体, 2:斜体, 3:粗斜体
        ),
        BarcodeElement(
            object_name="barcode-main",
            data="1234567890",
            barcode_type=BarcodeType.CODE_128_AUTO,
            x=5, y=20,
            scale=3, # 条码尺寸/模块大小
            height=10 # 一维码高度 (mm)
        ),
        ImageElement(
            object_name="logo-img",
            # 假设 'logo.png' 在脚本同目录下
            image_path=Path(__file__).parent / "logo.png",
            x=40, y=2,
            fixed_width=15, # 固定图片宽度为 15mm
            fixed_height=15 # 固定图片高度为 15mm
        )
    ]
    logger.info(f"创建了 {len(elements)} 个标签元素.")

    # 5. 预览标签
    logger.info("生成标签预览...")
    preview_image = sdk.preview_label(elements)
    if preview_image:
        # preview_image.show() # 直接显示预览图 (需要图形界面环境)
        preview_image.save("label_preview.png")
        logger.info("预览图已保存为 label_preview.png")
    else:
        logger.warning("生成预览失败.")

    # 6. 打印标签
    logger.info("准备打印标签...")
    # 检查打印机状态
    status_code, status_msg = sdk.get_printer_status()
    logger.info(f"打印前状态: 代码={status_code}, 信息='{status_msg}'")

    # 0 表示打印机正常待机
    if status_code == 0:
        print_result = sdk.print_label(elements, copies=1)
        logger.info(f"打印指令发送完成. 结果: {print_result}")
        if print_result.startswith("Error:"):
            logger.error(f"打印失败: {print_result}")
    # 96 表示剥纸器正在等待取走标签 (也认为是可打印状态)
    elif status_code == 96:
        logger.warning("打印机处于剥离模式，等待标签被取走。尝试打印...")
        print_result = sdk.print_label(elements, copies=1)
        logger.info(f"打印指令发送完成. 结果: {print_result}")
    else:
        logger.error(f"打印机状态异常 ({status_msg})，取消打印。")

except ZMPrinterStateError as e:
    logger.error(f"打印机状态错误: {e}")
except ZMPrinterCommandError as e:
    logger.error(f"打印命令执行错误: {e}")
except ImportError as e:
    logger.critical(f"SDK 初始化失败，可能是 .NET 环境或 DLL 问题: {e}")
except FileNotFoundError as e:
    logger.error(f"文件未找到 (例如图片或 LSF 文件): {e}")
except Exception as e:
    logger.exception(f"发生未知错误: {e}")

```

## 详细用法

### 1. 初始化 `LabelPrinterSDK`

```python
from zmprinter import LabelPrinterSDK, ZMPrinterImportError

try:
    # 自动查找 DLL (推荐)
    sdk = LabelPrinterSDK()
    # 初始化时可以直接传入 printer_config 和 label_config，后面打印时不需要每次都传入

    # 或者手动指定 DLL 完整路径
    # dll_path = "C:/path/to/your/libs/x64/LabelPrinter.dll"
    # sdk = LabelPrinterSDK(dll_path=dll_path)

except ZMPrinterImportError as e:
    print(f"加载 DLL 失败: {e}")
    print("请确保 DLL 文件存在、路径正确、.NET Framework 已安装且与 Python/DLL 架构匹配。")
    # 退出或采取其他错误处理
except Exception as e:
    print(f"初始化 SDK 时发生其他错误: {e}")
```

### 2. 配置打印机 (`PrinterConfig`)

`PrinterConfig` 用于设置打印机的连接方式和打印参数。

```python
from zmprinter import PrinterConfig, PrinterStyle

# USB 打印机 (常用)
usb_config = PrinterConfig(
    interface=PrinterStyle.USB,
    dpi=300,
    speed=4,
    darkness=12,
    has_gap=True, # 标签之间有间隙
    # mbsn="ZMB123456" # 可选，当有多台 USB 打印机时指定序列号
)

# 网络打印机
net_config = PrinterConfig(
    interface=PrinterStyle.NET,
    ip_address="192.168.1.100", # 打印机 IP 地址
    dpi=300,
    speed=4,
    darkness=10,
    has_gap=True
)

# Windows 驱动打印机
driver_config = PrinterConfig(
    interface=PrinterStyle.DRIVER,
    name="ZMPrinter ZM-LP110A(300dpi)", # 系统中显示的打印机名称
    dpi=300, # DPI 通常由驱动决定，这里设置可能无效
    # speed, darkness 通常也由驱动控制
)

# RFID USB 打印机
rfid_usb_config = PrinterConfig(
    interface=PrinterStyle.RFID_USB,
    dpi=300,
    speed=3,
    darkness=15, # RFID 打印通常需要更高浓度
    has_gap=True
)

# 其他配置项:
# page_direction: 1=纵向 (默认), 2=横向
# reverse: False=正常打印 (默认), True=反向打印
# print_num: 每次打印任务的份数 (默认 1)
# copy_num: 副本数 (默认 1)
```

### 3. 配置标签 (`LabelConfig`)

`LabelConfig` 用于定义标签纸的物理尺寸和布局。单位通常是毫米 (mm)。

```python
from zmprinter import LabelConfig

# 单排标签 (宽 60mm, 高 40mm, 行间距 2mm)
single_label = LabelConfig(
    width=60.0,
    height=40.0,
    gap=2.0
)

# 多排多列标签 (例如: 2 列 x 1 行, 标签 40x30, 列间距 3mm)
multi_column_label = LabelConfig(
    width=40.0,
    height=30.0,
    gap=2.0,
    column_gap=3.0,
    row_num=1,
    column_num=2
)

# 其他配置项:
# left_offset, top_offset: 打印内容的整体左右/上下微调 (mm)
# page_left_edges, page_right_edges: 页面左右边距 (mm)
# page_start_location: 起始打印位置 (0=左上, 1=右上, 2=左下, 3=右下)
# page_label_order: 多标签打印顺序 (0=水平, 1=垂直)
# label_shape: 标签形状 (0=圆角矩形, 1=方角矩形, 2=椭圆形)
```

### 4. 创建标签元素

所有元素都继承自 `LabelElement`，并需要一个唯一的 `object_name`。坐标 `x`, `y` 通常指元素左上角的起始位置 (mm)。

#### 文本 (`TextElement`)

```python
from zmprinter import TextElement

text1 = TextElement(
    object_name="product-name",
    data="超细纤维毛巾",
    x=5, y=5,
    font_name="宋体", # 打印机支持的字体
    font_size=10,
    font_style=1 # 粗体
)

# 多行文本 (自动换行)
multiline_text = TextElement(
    object_name="description",
    data="这是一款高质量的超细纤维毛巾，吸水性强，不掉毛，适用于家居清洁和汽车护理。",
    x=5, y=15,
    font_name="微软雅黑",
    font_size=8,
    is_multiline=True,
    width=50, # 指定文本区域宽度 (mm)
    text_align=0, # 0=左对齐, 1=居中, 2=右对齐
    text_valign=0 # 0=顶对齐, 1=垂直居中, 2=底对齐
)

# 黑底白字
reverse_text = TextElement(
    object_name="warning",
    data="注意",
    x=30, y=30,
    font_size=12,
    black_background=True
)
```

#### 条码/二维码 (`BarcodeElement`)

```python
from zmprinter import BarcodeElement, BarcodeType

# Code 128 条码
code128 = BarcodeElement(
    object_name="sn-code128",
    data="SN123456789",
    barcode_type=BarcodeType.CODE_128_AUTO,
    x=5, y=25,
    scale=3, # 粗细/模块大小
    height=12, # 一维码高度 (mm)
    text_position=0 # 0=文字在下方, 1=上方, 2=不显示
)

# QR Code 二维码
qrcode = BarcodeElement(
    object_name="link-qrcode",
    data="https://example.com",
    barcode_type=BarcodeType.QR_CODE,
    x=40, y=15,
    scale=3, # 模块大小 (值越大，码越小)
    error_correction=1 # 纠错等级 0=L, 1=M, 2=Q, 3=H
)

# GS1-128 条码 (需要符合 GS1 标准的数据格式)
gs1_128 = BarcodeElement(
    object_name="gtin-gs1",
    data="(01)01234567890128(10)BATCH001",
    barcode_type=BarcodeType.GS1_128,
    x=5, y=40,
    scale=3, height=10
)
```

#### 图片 (`ImageElement`)

支持从文件路径加载或直接提供图片 `bytes` 数据。

```python
from zmprinter import ImageElement
from pathlib import Path

# 从文件加载
logo_from_file = ImageElement(
    object_name="company-logo",
    image_path=Path(__file__).parent / "logo.png", # 使用 Path 对象
    x=45, y=5,
    fixed_width=10, # 固定宽度为 10mm
    aspect_ratio=True # 保持宽高比 (默认 True)
)

# 从 bytes 加载 (例如从网络下载或数据库读取)
try:
    with open(Path(__file__).parent / "icon.jpg", "rb") as f:
        image_bytes = f.read()
    icon_from_bytes = ImageElement(
        object_name="status-icon",
        image_data=image_bytes,
        x=50, y=25,
        fixed_width=8, fixed_height=8,
        aspect_ratio=False # 不保持宽高比
    )
except FileNotFoundError:
    print("警告: 图片文件未找到！")
    icon_from_bytes = None # 处理文件不存在的情况

elements = [logo_from_file]
if icon_from_bytes:
    elements.append(icon_from_bytes)
```

#### 图形 (`ShapeElement`)

用于绘制直线和矩形。

```python
from zmprinter import ShapeElement

# 水平线
hline = ShapeElement(
    object_name="divider-line",
    shape_type="line",
    start_x=5, start_y=15,
    end_x=55, end_y=15,
    line_width=0.5 # 线宽 (mm)
)

# 矩形框
rect_box = ShapeElement(
    object_name="border-rect",
    shape_type="rectangle",
    start_x=2, start_y=2,
    end_x=58, end_y=38,
    line_width=0.3
)

# 虚线 (line_dash_style: 0=实线, 1=破折, 2=点划, 3=点点划, 4=点)
dashed_line = ShapeElement(
    object_name="dashed",
    shape_type="line",
    start_x=10, start_y=35, end_x=50, end_y=35,
    line_width=0.3,
    line_dash_style=1
)
```

#### RFID (`RFIDElement`)

用于在打印时向 RFID 标签写入数据。坐标 (`x`, `y`) 对 RFID 元素无效。

```python
from zmprinter import RFIDElement, RFIDEncoderType, RFIDDataBlock, RFIDDataType

# 写入 UHF EPC 区 (16进制数据)
rfid_uhf_epc = RFIDElement(
    object_name="rfid-epc-write",
    data="E28011700000020F12345678", # 示例 EPC (确保长度和格式正确)
    rfid_encoder_type=RFIDEncoderType.UHF,
    rfid_data_block=RFIDDataBlock.EPC,
    rfid_data_type=RFIDDataType.HEX,
    rfid_error_times=1 # 写入失败重试次数
)

# 写入 UHF User 区 (文本数据, UTF-8 编码)
rfid_uhf_user = RFIDElement(
    object_name="rfid-user-write",
    data="产品序列号: XYZ-001",
    rfid_encoder_type=RFIDEncoderType.UHF,
    rfid_data_block=RFIDDataBlock.USER,
    rfid_data_type=RFIDDataType.TEXT,
    rfid_text_encoding=1 # 0=ASCII, 1=UTF-8
)

# 写入 HF/NFC 标签 (URL)
rfid_hf_ndef = RFIDElement(
    object_name="rfid-ndef-url",
    data="https://www.example.com/product/123",
    rfid_encoder_type=RFIDEncoderType.NFC, # 或 HF_15693, HF_14443A
    rfid_data_type=RFIDDataType.NDEF_URL,
    hf_start_block=4 # NDEF 通常从块 4 开始
)
```

### 5. 打印标签 (`print_label`)

将配置好的打印机、标签和元素列表传递给 `print_label` 方法。

```python
# elements 是包含 LabelElement 子类对象的列表
# printer_cfg, label_cfg 是配置对象

# 如果 sdk 实例化时已经传入了 printer_cfg, label_cfg，即
sdk = LabelPrinterSDK(printer_config=printer_cfg, label_config=label_cfg)
# 则后续打印时可以不需要手动传入 printer_cfg 和 label_cfg

# 打印 1 份
result = sdk.print_label(elements, copies=1)
print(f"打印结果: {result}")

# 打印 3 份，单独传入不同的 printer_cfg 和 label_cfg
result_multi = sdk.print_label(
    elements,
    copies=3,
    printer_config=printer_cfg_2,
    label_config=label_cfg_2,
)
print(f"多份打印结果: {result_multi}")

# 如果打印出错 (例如 RFID 写入失败)，result 会包含错误信息，如 "Error: RFID Write failed"
if result.startswith("Error:"):
    # 可以在这里调用 print_blank_page 排出错误标签
    # sdk.print_blank_page(printer_cfg, label_cfg, print_error_mark=True)
    pass
```

### 6. 预览标签 (`preview_label`)

生成标签的预览图，返回一个 Pillow `Image` 对象。

```python
preview = sdk.preview_label(elements)  # 同理，可单独传入不同的 printer_config 和 label_config
if preview:
    preview.show() # 显示图片
    preview.save("mylabel.png") # 保存为文件
else:
    print("无法生成预览图。")
```

### 7. 处理 LSF 文件

可以读取 `.lsf` 文件，获取其中的配置和元素，修改数据后再打印。

```python
from pathlib import Path
from zmprinter import ZMPrinterLSFError

lsf_file = Path(__file__).parent / "template.lsf"

try:
    # 读取 LSF 文件
    lsf_printer, lsf_label, lsf_elements, status = sdk.read_lsf(lsf_file)

    if status: # 如果 status 有内容，表示读取出错
        print(f"读取 LSF 文件失败: {status}")
    elif lsf_printer and lsf_label and lsf_elements:
        print("LSF 文件读取成功!")
        print(f"  打印机接口 (来自 LSF): {lsf_printer.interface.name}")
        print(f"  标签宽度 (来自 LSF): {lsf_label.width} mm")
        print(f"  找到 {len(lsf_elements)} 个元素。")

        # 更新 LSF 文件中的元素数据
        # 假设 LSF 文件中有一个名为 'variable-sku' 的文本元素或使用了同名变量
        new_sku = "SKU-NEW-001"
        updated = sdk.update_element_data(lsf_elements, "variable-sku", new_sku)
        if updated:
            print(f"  已更新元素/变量 'variable-sku' 的数据为: {new_sku}")
        else:
            print("  未找到名为 'variable-sku' 的元素或变量。")

        # 预览修改后的 LSF 标签
        lsf_preview = sdk.preview_label(lsf_elements)
        if lsf_preview:
            lsf_preview.save("lsf_preview_updated.png")
            print("  修改后的 LSF 预览图已保存。")

        # 使用从 LSF 读取的配置打印标签
        # print_result = sdk.print_label(lsf_printer, lsf_label, lsf_elements)
        # print(f"  打印 LSF 标签结果: {print_result}")

except ZMPrinterLSFError as e:
    print(f"处理 LSF 文件时出错: {e}")
except FileNotFoundError:
    print(f"错误: LSF 文件 '{lsf_file}' 未找到。")

```

### 8. RFID 标签读取

需要使用支持 RFID 的打印机接口 (`PrinterStyle.RFID_USB`, `PrinterStyle.RFID_NET` 等)。

```python
from zmprinter import ZMPrinterRFIDReadError, ZMPrinterConfigError

# 假设 printer_cfg 是 RFID_USB 或 RFID_NET 配置
# 假设 label_cfg 是对应的标签配置

try:
    # 读取 UHF 标签的 TID
    print("尝试读取 UHF TID...")
    # area: 0=TID, 1=EPC, 2=TID+EPC
    # stop_position: 0=原始位置, 1=撕纸位, 2=打印位, 3=写入位
    tid_data = sdk.read_uhf_tag(area=0, power=20, stop_position=2, timeout=1500)
    if tid_data:
        print(f"成功读取 TID: {tid_data}")
    else:
        print("未读取到 TID 或发生错误。")
        # 读取失败，可能需要排出标签
        # sdk.print_blank_page(printer_cfg, label_cfg)

    # 读取 UHF 标签的 EPC
    print("\n尝试读取 UHF EPC...")
    epc_data = sdk.read_uhf_tag(area=1, stop_position=2)
    if epc_data:
        print(f"成功读取 EPC: {epc_data}")
    else:
        print("未读取到 EPC 或发生错误。")

    # 读取 HF 标签的 UID (假设是 15693 协议)
    # print("\n尝试读取 HF UID...")
    # protocol: 1=15693, 2=14443A, 3=NFC
    # area: 0=UID, 1=Data Area
    # hf_uid = sdk.read_hf_tag(protocol=1, area=0, stop_position=1)
    # if hf_uid:
    #     print(f"成功读取 HF UID: {hf_uid}")
    # else:
    #     print("未读取到 HF UID 或发生错误。")

except ZMPrinterRFIDReadError as e:
    print(f"RFID 读取失败: {e}")
    # 排出标签
    # sdk.print_blank_page(printer_cfg, label_cfg, print_error_mark=True)
except ZMPrinterConfigError as e:
    print(f"配置错误: {e} (请确保使用了 RFID 接口)")
except Exception as e:
    print(f"读取 RFID 时发生未知错误: {e}")

```

### 9. 获取打印机状态 (`get_printer_status`)

返回一个包含状态码和状态描述的元组。

```python
status_code, status_message = sdk.get_printer_status()

print(f"打印机状态码: {status_code}")
print(f"状态信息: {status_message}")

if status_code == 0:
    print("打印机准备就绪。")
elif status_code == 83:
    print("标签错误 (可能缺纸或卡纸)。")
elif status_code == 88:
    print("打印机暂停。")
elif status_code == 89:
    print("标签用完。")
elif status_code == 90:
    print("RFID 读写错误。")
elif status_code < 0:
    print("通信错误或未连接。")
# ... 其他状态码请参考 SDK 文档或 core.py 中的注释
```

### 10. 获取 USB 打印机序列号 (`get_usb_printer_sn`)

返回连接到电脑的所有 ZMPrinter USB 打印机的主板序列号列表。

```python
sn_list = sdk.get_usb_printer_sn()
if sn_list:
    print("找到以下 USB 打印机 SN:")
    for sn in sn_list:
        print(f"  - {sn}")
    # 可以用第一个 SN 来配置打印机
    # printer_cfg.mbsn = sn_list[0]
else:
    print("未检测到 USB 打印机或获取 SN 失败。")
```

### 11. 发送原始指令 (`send_printer_command`)

如果需要直接发送打印机支持的原始指令 (如 ZPL, TSPL 等)，可以使用此方法。

```python
# 示例：发送 TSPL 指令设置打印速度 (需要打印机支持 TSPL)
tspl_command = 'SPEED 4\n'
result = sdk.send_printer_command(tspl_command)
print(f"发送 TSPL 指令结果: {result}")

# 示例：发送 ZPL 指令打印简单文本 (需要打印机支持 ZPL)
zpl_command = """
^XA
^FO50,50^ADN,36,20^FDHello ZPL^FS
^XZ
"""
result_zpl = sdk.send_printer_command(zpl_command)
print(f"发送 ZPL 指令结果: {result_zpl}")
```

### 12. 从 JSON 加载元素

`LabelElement.from_data` 类方法可以从符合 C# `LabelObject` 结构的字典创建相应的 Python 元素对象。这对于从配置文件或 API 接收数据创建标签很有用。参考 `tests/test_print_json.py` 中的示例。

```python
import json
from zmprinter import LabelElement

element_json = """
{
    "ObjectName": "text-from-json",
    "objectdata": "JSON 数据",
    "Xposition": 10,
    "Yposition": 10,
    "textfont": "黑体",
    "fontsize": 12
}
"""
element_dict = json.loads(element_json)
try:
    py_element = LabelElement.from_data(element_dict)
    if py_element:
        print(f"成功从 JSON 创建元素: {py_element.object_name}, 类型: {type(py_element).__name__}")
        # elements.append(py_element)
except ValueError as e:
    print(f"从 JSON 创建元素失败: {e}")
```

## 日志记录

SDK 使用 Python 内置的 `logging` 模块。可以通过以下方式配置：

*   **环境变量 (推荐):**
    *   `ZMPRINTER_LOG_LEVEL`: 设置日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)。默认 INFO。
    *   `ZMPRINTER_LOG_FORMAT`: 设置日志格式字符串。默认为 `"%(asctime)s - %(levelname)s - %(name)s - %(message)s"`。
*   **代码配置:**
    *   使用 `zmprinter.get_logger(name, log_level)` 获取指定名称和级别的 logger。
    *   使用 `zmprinter.setup_file_logging(filename, name, log_level)` 将日志同时输出到文件。
    *   直接使用导入的 `zmprinter.logger` 实例。

```python
import os
from zmprinter import get_logger, setup_file_logging, logger as default_logger

# 示例 1: 使用默认 logger (级别受环境变量影响)
default_logger.info("这是一条普通信息")
default_logger.debug("这条信息仅在 DEBUG 级别显示")

# 示例 2: 获取自定义 logger 并设置级别
my_logger = get_logger("my_app_module", log_level="DEBUG")
my_logger.debug("自定义 logger 的调试信息")

# 示例 3: 设置日志输出到文件
log_file_path = "app_print.log"
file_logger = setup_file_logging(log_file_path, name="file_output", log_level="INFO")
file_logger.warning("这条警告会写入文件和控制台")

# 查看 tests/test_logging.py 获取更详细的示例。
```

## 异常处理

SDK 定义了一系列继承自 `ZMPrinterError` 的异常类，用于指示不同的错误情况。建议在调用 SDK 方法时使用 `try...except` 块来捕获这些异常。

*   `ZMPrinterImportError`: 加载 DLL 或其依赖失败。
*   `ZMPrinterConfigError`: 提供的配置无效 (如接口类型错误、IP格式错误)。
*   `ZMPrinterInvalidElementError`: 创建或验证标签元素时出错。
*   `ZMPrinterCommunicationError`: 与打印机通信失败 (USB/网络)。
    *   `ZMPrinterUSBError`: USB 通信特定错误。
    *   `ZMPrinterNetworkError`: 网络通信特定错误。
*   `ZMPrinterStateError`: 打印机硬件状态错误 (如缺纸 `status_code=89`, 开盖等)。
*   `ZMPrinterCommandError`: 底层 DLL 执行命令时返回错误 (例如 `print_label` 返回 "Error: ...")。
*   `ZMPrinterLSFError`: 处理 LSF 文件时出错。
*   `ZMPrinterRFIDError`: RFID 操作通用错误。
    *   `ZMPrinterRFIDReadError`: 读取 RFID 标签失败。
    *   `ZMPrinterRFIDWriteError`: 写入 RFID 标签失败 (通常通过 `ZMPrinterCommandError` 表现)。
    *   `ZMPrinterRFIDTimeoutError`: RFID 操作超时。
*   `ZMPrinterDataError`: SDK 内部数据转换错误 (如图片处理)。

```python
from zmprinter import ZMPrinterError, ZMPrinterStateError

try:
    # ... SDK 操作 ...
    pass
except ZMPrinterStateError as e:
    print(f"打印机状态问题: {e}")
    # 可能需要提示用户检查打印机
except ZMPrinterCommandError as e:
    print(f"打印指令失败: {e}")
except ZMPrinterError as e:
    print(f"发生 ZMPrinter 相关错误: {e}")
except Exception as e:
    print(f"发生其他未知错误: {e}")
```

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

本项目使用 [MIT License](LICENSE) 授权。