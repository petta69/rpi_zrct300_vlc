import json
import usb.core

STREAMDECK_CONFIG = "streamdeck_ui_export.json"

ELGATO = {
    'USB_VID_ELGATO': 0x0fd9,
    'USB_PID_STREAMDECK_ORIGINAL': 0x0060,
    'USB_PID_STREAMDECK_ORIGINAL_V2': 0x006d,
    'USB_PID_STREAMDECK_MINI': 0x0063,
    'USB_PID_STREAMDECK_XL': 0x006c,
    'USB_PID_STREAMDECK_MK2': 0x0080,
    'USB_PID_STREAMDECK_PEDAL': 0x0086,
    'USB_PID_STREAMDECK_PLUS': 0x0084
}

def main():
    # find our device based on VendorId
    first_device = usb.core.find(idVendor=ELGATO["USB_VID_ELGATO"])

    ## If no devices found
    if first_device is None:
        raise ValueError('Device not found')

    ## Now match found device with known products
    found = False
    product = ""
    for item in ELGATO:
        if ELGATO[item] == first_device.idProduct:
            found = True
            product = item
            serial = first_device.serial_number

    if not found:
        raise ValueError('No defined Elgato devices found')

    print(f"Found product: {product} with serial: {serial}")


    ## Edit existing json setting file
    with open(STREAMDECK_CONFIG) as json_file:
            json_data = json.load(json_file)


    #test = json_data['state']
    key_list = list(json_data['state'].keys())
    json_data['state'][serial] = json_data['state'].pop(key_list[0])


    # Serializing json
    json_object = json.dumps(json_data, indent=4)
 
    # Writing file
    with open(STREAMDECK_CONFIG, "w") as outfile:
        outfile.write(json_object)


    print(f"Done with updating file: {STREAMDECK_CONFIG}")

if __name__ == "__main__":
     main()
