import json
from typing import List

from zmprinter import (
    LabelPrinterSDK,
    PrinterConfig,
    LabelConfig,
    LabelElement,
    BarcodeElement,
    PrinterStyle,
    LabelElementType,
)

json_string = """
{
    "Printer": {
        "printerinterface": "RFID_USB",
        "printnum": 1,
        "printerdpi": 300,
        "printSpeed": 4,
        "printDarkness": 18,
        "printermbsn": "",
        "printernetip": ""
    },
    "LabelFormat": {
        "labelwidth": 103,
        "labelheight": 40,
        "labelrowgap": 4
    },
    "LabelObjectList": [
        {
            "ObjectName": "rfiduhf-01",
            "objectdata": "CeJoo11KpTQm",
            "Xposition": 2,
            "Yposition": 2,
            "barcodekind": "Code 128 Auto",
            "barcodescale": 1,
            "barcodeheight": 10,
            "barcodealign": 0,
            "textposition": 0,
            "textfont": "黑体",
            "fontsize": 10,
            "texttextalign": 0,
            "texttextvalign": 0,
            "rectangleclass": 0,
            "cornerRadius": 2,
            "startXposition": 1,
            "startYposition": 1,
            "endXposition": 3,
            "endYposition": 3,
            "lineWidth": 0.4,
            "lineDashStyle": 0,
            "fillRectangle": false,
            "imagedata": "",
            "RFIDEncodertype": 0,
            "RFIDDatablock": 0,
            "RFIDDatatype": 0,
            "RFIDtidcontrol": 0,
            "DataAlignment": 0,
            "RFIDTextencoding": 1,
            "RFIDerrortimes": 1,
            "HFstartblock": 0
        },
        {
            "ObjectName": "text-3",
            "objectdata": "CeJoo11KpTQm",
            "Xposition": 78.4498749,
            "Yposition": 20.3899975,
            "barcodekind": "Code 128 Auto",
            "barcodescale": 1,
            "barcodeheight": 10,
            "barcodealign": 0,
            "textposition": 0,
            "textfont": "微软雅黑",
            "fontsize": 4.5,
            "texttextalign": 0,
            "texttextvalign": 0,
            "rectangleclass": 0,
            "cornerRadius": 2,
            "startXposition": 1,
            "startYposition": 1,
            "endXposition": 3,
            "endYposition": 3,
            "lineWidth": 0.4,
            "lineDashStyle": 0,
            "fillRectangle": false,
            "imagedata": "",
            "RFIDEncodertype": 0,
            "RFIDDatablock": 0,
            "RFIDDatatype": 0,
            "RFIDTextencoding": 0,
            "RFIDerrortimes": 2,
            "HFstartblock": 0
        },
        {
            "ObjectName": "barcode-1-42",
            "objectdata": "25041700001",
            "Xposition": 78.02,
            "Yposition": 23.51,
            "barcodekind": "Code 128 Auto",
            "barcodescale": 1.5,
            "barcodeheight": 6.56,
            "barcodealign": 0,
            "textposition": 0,
            "textfont": "微软雅黑",
            "fontsize": 3,
            "texttextalign": 0,
            "texttextvalign": 0,
            "rectangleclass": 0,
            "cornerRadius": 2,
            "startXposition": 1,
            "startYposition": 1,
            "endXposition": 3,
            "endYposition": 3,
            "lineWidth": 0.4,
            "lineDashStyle": 0,
            "fillRectangle": false,
            "imagedata": "",
            "RFIDEncodertype": 0,
            "RFIDDatablock": 0,
            "RFIDDatatype": 1,
            "RFIDTextencoding": 0,
            "RFIDerrortimes": 2,
            "HFstartblock": 0
        },
        {
            "ObjectName": "text-2",
            "objectdata": "1",
            "Xposition": 77.95986,
            "Yposition": 9.120001,
            "barcodekind": "Code 128 Auto",
            "barcodescale": 1,
            "barcodeheight": 10,
            "barcodealign": 0,
            "textposition": 0,
            "textfont": "微软雅黑",
            "fontsize": 5,
            "texttextalign": 0,
            "texttextvalign": 0,
            "rectangleclass": 0,
            "cornerRadius": 2,
            "startXposition": 1,
            "startYposition": 1,
            "endXposition": 3,
            "endYposition": 3,
            "lineWidth": 0.4,
            "lineDashStyle": 0,
            "fillRectangle": false,
            "imagedata": "",
            "RFIDEncodertype": 0,
            "RFIDDatablock": 0,
            "RFIDDatatype": 1,
            "RFIDTextencoding": 0,
            "RFIDerrortimes": 2,
            "HFstartblock": 0
        },
        {
            "ObjectName": "text-1",
            "objectdata": "2504170000",
            "Xposition": 77.96986,
            "Yposition": 12.6299973,
            "barcodekind": "Code 128 Auto",
            "barcodescale": 1,
            "barcodeheight": 10,
            "barcodealign": 0,
            "textposition": 0,
            "textfont": "微软雅黑",
            "fontsize": 5.5,
            "texttextalign": 0,
            "texttextvalign": 0,
            "rectangleclass": 0,
            "cornerRadius": 2,
            "startXposition": 1,
            "startYposition": 1,
            "endXposition": 3,
            "endYposition": 3,
            "lineWidth": 0.4,
            "lineDashStyle": 0,
            "fillRectangle": false,
            "imagedata": "",
            "RFIDEncodertype": 0,
            "RFIDDatablock": 0,
            "RFIDDatatype": 1,
            "RFIDTextencoding": 0,
            "RFIDerrortimes": 2,
            "HFstartblock": 0
        }
    ],
    "Operate": "preview"
}
"""


def print_from_json(json_payload: str):
    """
    Parses the JSON payload and uses the SDK to print the label.
    """
    try:
        print("Parsing JSON data...")
        data = json.loads(json_payload)

        # --- 1. Create Printer Config ---
        printer_data = data.get("Printer", {})
        interface_str = printer_data.get("printerinterface", "USB")  # Default if missing
        try:
            # Convert string name to Enum member
            interface_enum = PrinterStyle[interface_str.upper()]
        except KeyError:
            print(f"Error: Invalid printer interface '{interface_str}' in JSON. Defaulting to USB.")
            interface_enum = PrinterStyle.USB

        printer_cfg = PrinterConfig(
            interface=interface_enum,
            dpi=printer_data.get("printerdpi", 300),
            speed=printer_data.get("printSpeed", 4),
            darkness=printer_data.get("printDarkness", 10),
            mbsn=printer_data.get("printermbsn") or None,  # Use None if empty string
            ip_address=printer_data.get("printernetip") or None,  # Use None if empty string
            has_gap=True,  # Assuming labels have gaps unless specified otherwise
        )
        print(f"Printer Config: {printer_cfg.__dict__}")

        # Get number of copies
        copies = printer_data.get("printnum", 1)
        print(f"Copies: {copies}")

        # --- 2. Create Label Config ---
        label_data = data.get("LabelFormat", {})
        label_cfg = LabelConfig(
            width=label_data.get("labelwidth", 60),
            height=label_data.get("labelheight", 40),
            gap=label_data.get("labelrowgap", 2),
        )
        print(f"Label Config: {label_cfg.__dict__}")

        # --- 3. Create Label Elements ---
        elements: List[LabelElementType] = []
        object_list = data.get("LabelObjectList", [])
        print(f"Processing {len(object_list)} label elements...")

        for obj_data in object_list:
            py_element = LabelElement.from_data(obj_data)

            if isinstance(py_element, BarcodeElement):
                print(f"Scale: {py_element.scale}")

            if py_element:
                elements.append(py_element)
                print(f"    Added element: {py_element.__class__.__name__} - {py_element.object_name}")

        sdk_instance = LabelPrinterSDK(
            printer_config=printer_cfg,
            label_config=label_cfg,
        )

        # --- 4. Perform Print Operation ---
        openrate = data.get("Operate")
        if openrate == "print":
            if not elements:
                print("Error: No valid label elements were created. Cannot print.")
                return sdk_instance

            print("\nChecking printer status before printing...")
            status_code, status_msg = sdk_instance.get_printer_status(printer_cfg)
            print(f"Printer Status: {status_code} - {status_msg}")

            if status_code == 0 or status_code == 96:  # 0: Ready, 96: Waiting for label removal (might be ok)
                print(f"\nAttempting to print {copies} copies...")
                print_result = sdk_instance.print_label(elements, copies=copies)
                print(f"\nPrint command finished. Result: {print_result}")
            else:
                print("\nPrinter not ready. Print operation cancelled.")
        elif openrate == "preview":
            print("\nPreviewing label...")
            preview_result = sdk_instance.preview_label(elements)
            print(f"\nPreview command finished. Result: {preview_result}")
            if preview_result:
                preview_result.show()
            return sdk_instance
        else:
            print(f"\nOperation specified is '{data.get('Operate', 'None')}', not 'print'. No print action taken.")

    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON payload. {e}")
    except ImportError as e:
        print(f"Error: SDK Initialization failed (ImportError). {e}")
    except RuntimeError as e:
        print(f"Error: SDK Runtime error. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    try:
        # Call the function to process the JSON and print
        print_from_json(json_string)

    except ImportError as e:
        print(f"Fatal Error: Could not initialize LabelPrinter SDK. {e}")
        print("Please ensure LabelPrinter.dll is accessible and required .NET framework is installed.")
    except Exception as e:
        print(f"Fatal Error during SDK setup or execution: {e}")
