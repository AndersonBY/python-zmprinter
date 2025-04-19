#!/usr/bin/env python3
"""
Barcode label creation and preview. Optionally print to printer.
"""

import os
import argparse
from typing import List

from zmprinter import LabelPrinterSDK, PrinterConfig, LabelConfig
from zmprinter.elements import BarcodeElement, LabelElementType
from zmprinter.enums import BarcodeType


def create_barcode_label(data_str: str, cfg: LabelConfig) -> List[LabelElementType]:
    # Generate a simple barcode element in center
    barcode = BarcodeElement(
        object_name="barcode-01",
        data=data_str,
        barcode_type=BarcodeType.CODE_128_AUTO,
        x=10.0,
        y=5.0,
        scale=4,
        height=15.0,
    )
    return [barcode]


def main():
    parser = argparse.ArgumentParser(description="Barcode Label Example")
    parser.add_argument("-d", "--data", required=True, help="Data to encode in the barcode")
    parser.add_argument("--print", action="store_true", help="Actually send to printer")
    args = parser.parse_args()

    sdk = LabelPrinterSDK()
    printer_cfg = PrinterConfig()
    label_cfg = LabelConfig(width=60.0, height=40.0)

    elements = create_barcode_label(args.data, label_cfg)
    preview = sdk.preview_label(elements, printer_cfg, label_cfg)
    if preview:
        os.makedirs("output", exist_ok=True)
        preview_path = os.path.join("output", "barcode_preview.png")
        preview.save(preview_path)
        print(f"Barcode preview saved to {preview_path}")
    else:
        print("Preview generation failed.")

    if args.print:
        result, count = sdk.print_label(
            elements, copies=1, stop_at_error=True, printer_config=printer_cfg, label_config=label_cfg
        )
        print(f"Print result: {result}, printed: {count}")


if __name__ == "__main__":
    main()
