import time
from typing import Optional

from zmprinter import (
    LabelPrinterSDK,
    ZMPrinterError,
    ZMPrinterImportError,
    logger,
)
from test_print_json import print_from_json, json_string


# Monitoring parameters
POLLING_INTERVAL_SECONDS = 0.5  # How often to check status (seconds)
MONITORING_TIMEOUT_SECONDS = 15  # Max time to monitor after sending print job

# --- Main Script ---
if __name__ == "__main__":
    logger.info("--- ZMPrinter Print and Monitor Test ---")

    sdk: Optional[LabelPrinterSDK] = None
    try:
        sdk = print_from_json(json_string)
        if sdk is None:
            raise ZMPrinterError("Failed to initialize SDK")

        # --- 6. Start Monitoring Loop ---
        logger.info(
            f"Starting status monitoring loop (Interval: {POLLING_INTERVAL_SECONDS}s, Timeout: {MONITORING_TIMEOUT_SECONDS}s)..."
        )
        start_time = time.time()
        last_status_code = -999  # Initialize with a value that's not 0 or 96
        consecutive_ready_count = 0
        monitoring_complete = False

        while time.time() - start_time < MONITORING_TIMEOUT_SECONDS:
            try:
                current_status_code, current_status_msg = sdk.get_printer_status()

                # Log only if status changes or it's the first check
                if current_status_code != last_status_code:
                    logger.info(f"Status Update: Code={current_status_code}, Message='{current_status_msg}'")
                    last_status_code = current_status_code

                    # Reset consecutive ready counter if status is not ready/waiting
                    if current_status_code not in [0, 96]:
                        consecutive_ready_count = 0

                # --- Completion Logic ---
                # Check if printer has returned to a ready/waiting state
                if current_status_code in [0, 96]:
                    consecutive_ready_count += 1
                    # Require seeing ready/waiting status a couple of times consecutively
                    # to be more confident printing is done. Adjust threshold as needed.
                    if consecutive_ready_count >= 2:
                        logger.info(
                            f"Printer returned to ready/waiting state (Code: {current_status_code}). Assuming print job complete."
                        )
                        monitoring_complete = True
                        break
                # Check for specific error conditions that indicate failure/stop
                elif current_status_code not in [4]:  # Ignore '4' (Printing) if it ever appears
                    # Codes like 81, 82, 83, 88, 89, 90, 91, 92 or negative codes indicate issues
                    logger.warning(
                        f"Printer entered non-ready state (Code: {current_status_code}). Stopping monitoring."
                    )
                    monitoring_complete = True
                    break

            except ZMPrinterError as e:
                logger.exception(f"Error during status polling: {e}")
                monitoring_complete = True  # Stop monitoring on error
                break
            except Exception as e:
                logger.exception(f"Unexpected error during status polling: {e}")
                monitoring_complete = True  # Stop monitoring on error
                break

            time.sleep(POLLING_INTERVAL_SECONDS)

        # --- 7. Post-Monitoring ---
        if not monitoring_complete:
            logger.warning(f"Monitoring timed out after {MONITORING_TIMEOUT_SECONDS} seconds.")

        logger.info("Checking final printer status...")
        final_status_code, final_status_msg = sdk.get_printer_status(sdk.printer_config)
        logger.info(f"Final Status: Code={final_status_code}, Message='{final_status_msg}'")
        logger.info("--- Test Finished ---")

    except ZMPrinterImportError as e:
        logger.critical(f"Failed to import or load LabelPrinter SDK: {e}")
        logger.critical("Please ensure LabelPrinter.dll is accessible and required .NET framework is installed.")
    except ZMPrinterError as e:
        logger.error(f"A ZMPrinter specific error occurred: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
    finally:
        # Optional: any cleanup if needed
        pass
