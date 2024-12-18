# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support

from board import *
import board
import digitalio
import storage
import usb_cdc
import usb_hid
import usb_midi
import supervisor

# Define identificación personalizada USB
CUSTOM_VID = 0x413C                       # VID personalizado
CUSTOM_PID = 0x2003                       # PID personalizado
PRODUCT_NAME = "Dell USB Entry Keyboard"  # Nombre del producto
MANUFACTURER_NAME = "Dell Computer Corp." # Nombre del fabricante

# Configura la identificación USB
supervisor.set_usb_identification(vid=CUSTOM_VID, pid=CUSTOM_PID, manufacturer=MANUFACTURER_NAME, product=PRODUCT_NAME)


# Desactiva otros dispositivos USB que no se necesiten
usb_midi.disable()
usb_cdc.disable()
usb_hid.enable((usb_hid.Device.KEYBOARD,))

# Configuración para activar/desactivar almacenamiento según el estado del botón BOOTSEL
noStoragePin = digitalio.DigitalInOut(board.GP15)
noStoragePin.switch_to_input(pull=digitalio.Pull.UP)

# Si BOOTSEL está presionado (GP15 a bajo), activa CIRCUITPY
if noStoragePin.value:
    # Modo sin almacenamiento (solo teclado HID)
    storage.disable_usb_drive()
    print("USB drive disabled; HID mode only")
else:
    # Modo con CIRCUITPY visible
    storage.enable_usb_drive()
    print("USB drive enabled; CIRCUITPY mode")

# Limpia el pin
noStoragePin.deinit()

