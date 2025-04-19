#!/usr/bin/env python3
"""
Simple label preview example.
Generates a preview image with a single text element.
"""
import os

from zmprinter import LabelPrinterSDK, PrinterConfig, LabelConfig
from zmprinter.elements import TextElement


def main():
    # Initialize SDK (uses default DLL detection)
    sdk = LabelPrinterSDK()

    # Configure printer and label (adjust parameters as needed)
    printer_cfg = PrinterConfig()  # Default: USB, 300dpi, speed=4, darkness=10
    label_cfg = LabelConfig(width=50.0, height=30.0)  # Label size: 50mm x 30mm

    # Create a text element at position (5,5)
    text = TextElement(
        object_name="text-01",
        data="Hello ZMPrinter!",
        x=5.0,
        y=5.0,
    )

    # Generate preview image
    image = sdk.preview_label([text], printer_cfg, label_cfg)
    if image:
        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", "simple_preview.png")
        image.save(output_path)
        print(f"Label preview saved to {output_path}")
    else:
        print("Failed to generate label preview.")


if __name__ == "__main__":
    main()
