from pathlib import Path

from zmprinter import (
    LabelPrinterSDK,
    PrinterConfig,
    LabelConfig,
    PrinterStyle,
    BarcodeType,
    RFIDEncoderType,
    RFIDDataBlock,
    RFIDDataType,
    TextElement,
    ShapeElement,
    BarcodeElement,
    RFIDElement,
    ImageElement,
)

try:
    # 1. 初始化 SDK (确保 LabelPrinter.dll 在路径中或提供完整路径)
    # sdk = LabelPrinterSDK(dll_path="C:\\path\\to\\your\\libs\\AnyCPU\\LabelPrinter.dll")
    sdk = LabelPrinterSDK()  # 尝试自动查找

    # 2. 定义打印机配置 (USB 示例)
    printer_cfg = PrinterConfig(interface=PrinterStyle.USB, dpi=300, speed=4, darkness=10, has_gap=True)

    # 或者 网络打印机示例
    # printer_cfg_net = PrinterConfig(
    #     interface=PrinterStyle.NET,
    #     ip_address="192.168.1.180",
    #     dpi=300,
    #     speed=4,
    #     darkness=10
    # )

    # 或者 RFID USB 打印机示例
    printer_cfg_rfid = PrinterConfig(interface=PrinterStyle.RFID_USB, dpi=300, speed=4, darkness=12, has_gap=True)

    # 3. 定义标签配置
    label_cfg = LabelConfig(width=100, height=30, gap=2)

    # 4. 定义标签元素
    elements = [
        TextElement(
            object_name="text-01",  # C# 示例中的名称
            data="简体：葡国2号李奥红酒 19 Borge Douro Lello Tinto 375ml",
            x=25,
            y=35,  # 注意 C# 示例的坐标可能基于不同的原点或单位系统，这里假设是 mm
            font_name="宋体",
            font_size=8,
            font_style=1,
            is_multiline=True,
            width=50,
            text_align=1,
            text_valign=1,  # 居中
        ),
        ShapeElement(
            object_name="rectangle-01",
            shape_type="rectangle",
            start_x=24,
            start_y=25,
            end_x=76,
            end_y=45,
            line_width=0.4,
        ),
        TextElement(
            object_name="text-02",
            data="繁体：茅臺紀念酒 澳門城市大學（陳釀）+愛士圖爾套裝",
            x=5,
            y=6,
            font_name="黑体",
            font_size=10,
        ),
        BarcodeElement(
            object_name="barcode-01",
            data="(01)06975503990001(21)2307010001",  # GS1-128 数据
            barcode_type=BarcodeType.GS1_128,  # C# 示例用的 GS1-128
            x=25,
            y=12,
            scale=3,
            height=5,
        ),
        ImageElement(
            object_name="image-01",
            image_path=Path(__file__).parent / "cat.png",
            x=10,
            y=10,
            fixed_width=20,
            fixed_height=20,
        ),
        RFIDElement(  # RFID 写入示例 (仅在打印时生效)
            object_name="rfiduhf-01",
            data="1234567890ABCDEF12345678",  # 示例 EPC (16进制)
            rfid_encoder_type=RFIDEncoderType.UHF,
            rfid_data_block=RFIDDataBlock.EPC,
            rfid_data_type=RFIDDataType.HEX,
            rfid_error_times=1,
        ),
    ]

    # 5. 预览标签
    print("生成预览...")
    preview_image = sdk.preview_label(printer_cfg, label_cfg, elements)
    if preview_image:
        preview_image.show()  # 使用 Pillow 显示图片
        # preview_image.save("preview.png") # 保存图片
        print("预览图已生成并显示 (或保存)。")
    else:
        print("生成预览失败。")

    # 6. 打印标签 (使用 RFID 配置)
    print("\n准备打印...")
    # 检查状态
    status_code, status_msg = sdk.get_printer_status(printer_cfg_rfid)
    print(f"打印前状态: {status_code} - {status_msg}")

    if status_code == 0:  # 仅在状态正常时打印
        # 打印前更新条码数据
        sdk.update_element_data(elements, "barcode-01", "(01)06975503990001(21)2307019999")
        sdk.update_element_data(elements, "rfiduhf-01", "FEDCBA9876543210FEDCBA98")  # 更新 RFID 数据

        print_result = sdk.print_label(printer_cfg_rfid, label_cfg, elements, copies=1)
        print(f"打印结果: {print_result}")
    else:
        print("打印机状态异常，取消打印。")

    # 7. 读取 LSF 文件示例
    print("\n读取 LSF 文件...")
    try:
        lsf_printer, lsf_label, lsf_elements, lsf_status = sdk.read_lsf(Path(__file__).parent / "test.lsf")
        if lsf_status or not lsf_printer or not lsf_label or not lsf_elements:
            print(f"读取 LSF 失败: {lsf_status}, {lsf_printer}, {lsf_label}, {lsf_elements}")
        else:
            print("LSF 文件读取成功!")
            print(f"  打印机 DPI (从 LSF): {lsf_printer.dpi}")
            print(f"  标签宽度 (从 LSF): {lsf_label.width} mm")
            print(f"  找到 {len(lsf_elements)} 个元素:")
            for elem in lsf_elements:
                print(f"    - {elem.object_name} ({type(elem).__name__}): {elem.data}")

            # 更新 LSF 中的变量
            update_success = sdk.update_element_data(lsf_elements, "text-2", "高级 Python 笔记本")
            if update_success:
                print("  已更新 LSF 元素 'text-2' 的数据。")
            else:
                print("  未找到名为 'text-2' 的 LSF 元素或变量。")

            # 预览 LSF 标签
            lsf_preview = sdk.preview_label(lsf_printer, lsf_label, lsf_elements)
            if lsf_preview:
                lsf_preview.show()
                print("  LSF 预览图已显示。")

            # 打印 LSF 标签 (需要确保打印机配置正确)
            # print_lsf_result = sdk.print_label(lsf_printer, lsf_label, lsf_elements, copies=1)
            # print(f"  打印 LSF 结果: {print_lsf_result}")

    except FileNotFoundError:
        print("LSF 文件未找到，跳过 LSF 示例。")
    except Exception as e:
        print(f"处理 LSF 时出错: {e}")

    # 8. 读取 RFID 标签示例 (TID)
    print("\n尝试读取 UHF TID...")
    # 假设使用 printer_cfg_rfid
    tid_data = sdk.read_uhf_tag(printer_cfg_rfid, label_cfg, area=0, stop_position=2)  # 读取 TID，停在打印位置
    if tid_data.startswith("Error:"):
        print(f"读取 TID 失败: {tid_data}")
    elif not tid_data:
        print("未读取到 TID 数据。")
        # sdk.print_blank_page(printer_cfg_rfid, label_cfg) # 排出标签
    else:
        print(f"成功读取到 TID: {tid_data}")
        # 可以用读取到的 TID 更新元素并打印
        # sdk.update_element_data(elements, "barcode-01", tid_data)
        # print_tid_result = sdk.print_label(printer_cfg_rfid, label_cfg, elements, copies=1)
        # print(f"打印 TID 结果: {print_tid_result}")

    # 9. 获取 USB 打印机 SN 列表
    print("\n获取连接的 USB 打印机 SN...")
    sn_list = sdk.get_usb_printer_sn()
    if sn_list:
        print(f"找到 USB 打印机 SN: {', '.join(sn_list)}")
    else:
        print("未找到连接的 USB 打印机或获取失败。")

except ImportError as e:
    print(f"初始化 SDK 失败: {e}")
    print("请确保 LabelPrinter.dll 可访问并且已安装所需的 .NET Framework。")
except Exception as e:
    print(f"运行 SDK 时发生意外错误: {e}")
