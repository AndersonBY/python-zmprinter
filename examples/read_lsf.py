#!/usr/bin/env python3
"""
Read an existing LSF label file and preview it.
"""

import os
import argparse
import pprint

from zmprinter import LabelPrinterSDK


def main():
    parser = argparse.ArgumentParser(description="LSF Label File Reader Example")
    parser.add_argument("-f", "--file", required=True, help="Path to the .lsf label file")
    args = parser.parse_args()

    sdk = LabelPrinterSDK()
    # Read LSF file
    print(f"Reading LSF file: {args.file}")
    printer_cfg, label_cfg, elements, status = sdk.read_lsf(args.file)
    if status:
        print(f"Error reading LSF file: {status}")
        return

    # Display parsed configuration
    print("Printer Config:")
    pprint.pprint(printer_cfg.__dict__ if printer_cfg else {})

    print("Label Config:")
    pprint.pprint(label_cfg.__dict__ if label_cfg else {})

    print(f"Parsed {len(elements) if elements else 0} elements:")
    if elements:
        for elem in elements:
            print(f" - {elem.object_name}: {elem.__class__.__name__}")

    # Generate preview image
    if printer_cfg and label_cfg and elements:
        try:
            preview = sdk.preview_label(elements, printer_cfg, label_cfg)
            if preview:
                os.makedirs("output", exist_ok=True)
                out_path = os.path.join("output", "lsf_preview.png")
                preview.save(out_path)
                print(f"LSF label preview saved to {out_path}")
            else:
                print("Failed to generate preview for LSF file.")
        except Exception as e:
            print(f"Error generating preview: {e}")


if __name__ == "__main__":
    main()
