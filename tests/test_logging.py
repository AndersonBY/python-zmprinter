#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zmprinter 日志功能使用示例
"""

import os
import sys
from pathlib import Path

# 添加项目路径到Python路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# 导入zmprinter
from src.zmprinter import (
    PrinterConfig,
    LabelConfig,
    PrinterStyle,
    TextElement,
    get_logger,
    setup_file_logging,
    logger as zmprinter_logger,
)

# 方法1: 使用环境变量设置日志级别
# 设置环境变量可以在运行前配置
os.environ["ZMPRINTER_LOG_LEVEL"] = "DEBUG"
os.environ["ZMPRINTER_LOG_FORMAT"] = "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"


# 方法2: 直接使用包导出的logger实例
def use_package_logger():
    zmprinter_logger.info("使用包导出的logger")
    zmprinter_logger.debug("这是一条调试信息")
    zmprinter_logger.warning("这是一条警告信息")

    # 测试异常记录
    try:
        raise ValueError("这是一个测试异常")
    except Exception as e:
        zmprinter_logger.exception(f"捕获到异常: {e}")


# 方法3: 获取一个自定义名称的logger
def use_custom_logger():
    # 获取自定义logger
    custom_logger = get_logger("custom_module", log_level="DEBUG")
    custom_logger.info("使用自定义logger")
    custom_logger.debug("这条信息只在DEBUG级别可见")


# 方法4: 同时输出到文件和控制台
def setup_file_logger():
    # 设置文件日志
    log_file = Path(__file__).parent / "zmprinter.log"
    file_logger = setup_file_logging(filename=str(log_file), name="file_logger", log_level="INFO")

    file_logger.info(f"日志记录到文件: {log_file}")
    file_logger.debug("这条信息不会记录到文件，因为文件日志级别是INFO")
    file_logger.warning("警告信息会记录到文件和控制台")

    return str(log_file)


# 方法5: 在实际应用中使用logger
def simulate_printing():
    app_logger = get_logger("app")

    try:
        app_logger.info("初始化标签打印")

        # 创建打印机配置
        printer_config = PrinterConfig(interface=PrinterStyle.DRIVER, name="Windows打印机名称", dpi=300)

        # 创建标签配置
        label_config = LabelConfig(width=50, height=30)

        # 创建标签元素
        text = TextElement(object_name="text-01", data="Hello Logger!", x=10, y=10, font_name="Arial", font_size=12)

        app_logger.debug(f"创建了文本元素: {text.object_name} = '{text.data}'")

        # 模拟一个错误
        app_logger.error("模拟一个打印错误")

    except Exception as e:
        app_logger.exception(f"打印过程中发生异常: {e}")


if __name__ == "__main__":
    print("=== zmprinter日志功能示例 ===")

    # 演示不同的日志使用方式
    use_package_logger()
    use_custom_logger()
    log_file = setup_file_logger()
    simulate_printing()

    print(f"\n日志文件保存在: {log_file}")
    print("查看控制台输出和日志文件以了解不同日志级别的信息")
