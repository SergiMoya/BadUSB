import os
import time
import shutil

# Rutas de los archivos necesarios
nuke_file = "flash_nuke.uf2"
uf2_file = "adafruit-circuitpython-raspberry_pi_pico-en_US-8.0.0.uf2"
lib_files = ["adafruit_hid", "asyncio", "adafruit_debouncer.mpy", "adafruit_ticks.mpy", "keyboard_layout_win_es.mpy", "keycode_win_es.mpy", "adafruit_wsgi", "consumer_control_extended.mpy", "keyboard_layout.mpy"]
main_files = ["boot.py", "code.py", "duckyinpython.py", "payload.dd"]

# Función para verificar si la unidad está disponible
def check_drive(drive_letter, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(drive_letter):
            print(f"Unidad {drive_letter} detectada.")
            return drive_letter
        print(f"Esperando que se detecte la unidad {drive_letter}...")
        time.sleep(3)
    print(f"Error: No se detectó la unidad {drive_letter} después de {timeout} segundos.")
    return None

# Solicitar al usuario que ingrese solo la letra de la unidad
drive_letter = input("Introduce la letra de la unidad USB (por ejemplo, 'E'): ").strip()

# Añadir los dos puntos ':' automáticamente
drive_letter = drive_letter + ":\\"

# Validar que la entrada sea válida (debe ser una sola letra)
if len(drive_letter) != 3 or not drive_letter[0].isalpha() or drive_letter[1] != ":":
    print("Error: La letra de la unidad debe ser válida (por ejemplo, 'E').")
    exit(1)

# Paso 1: Detectar la unidad y copiar el archivo flash_nuke.uf2
print(f"Buscando unidad {drive_letter}...")
rp_drive = check_drive(drive_letter)

if rp_drive is None:
    print(f"Error: La unidad {drive_letter} no se encontró. Asegúrate de que el dispositivo esté conectado y en modo de almacenamiento USB.")
    exit(1)

print(f"Unidad {rp_drive} detectada. Copiando el archivo flash_nuke.uf2 para reiniciar...")
try:
    shutil.copy(nuke_file, rp_drive)
    print("Archivo flash_nuke.uf2 copiado correctamente. Esperando reinicio...")
except Exception as e:
    print(f"Error al copiar el archivo flash_nuke.uf2: {e}")
    exit(1)

# Esperar unos segundos para que el dispositivo se reinicie
time.sleep(5)

# Paso 2: Detectar nuevamente la unidad y copiar el archivo de CircuitPython
print(f"Buscando unidad {drive_letter} nuevamente para copiar CircuitPython...")
rp_drive = check_drive(drive_letter)

if rp_drive is None:
    print(f"Error: La unidad {drive_letter} no se encontró después de reiniciar. Asegúrate de que el dispositivo esté conectado y en modo de almacenamiento USB.")
    exit(1)

print(f"Unidad {rp_drive} detectada. Copiando el archivo UF2 de CircuitPython...")
try:
    shutil.copy(uf2_file, rp_drive)
    print("Archivo UF2 de CircuitPython copiado correctamente. Esperando reinicio...")
except Exception as e:
    print(f"Error al copiar el archivo UF2 de CircuitPython: {e}")
    exit(1)

# Esperar unos segundos para que el dispositivo se reinicie
time.sleep(5)

# Paso 3: Detectar nuevamente la unidad como CIRCUITPY
print(f"Buscando unidad {drive_letter} como CIRCUITPY...")
circuitpy_drive = check_drive(drive_letter)

if circuitpy_drive is None:
    print(f"Error: La unidad {drive_letter} no se detectó como CIRCUITPY. Asegúrate de que el dispositivo haya reiniciado correctamente.")
    exit(1)

# Crear la carpeta 'lib' si no existe
lib_path = os.path.join(circuitpy_drive, "lib")
try:
    os.makedirs(lib_path, exist_ok=True)
    print("Carpeta 'lib' creada correctamente.")
except Exception as e:
    print(f"Error al crear la carpeta 'lib': {e}")
    exit(1)

# Paso 4: Copiar los archivos específicos de librerías en la carpeta 'lib'
print("Copiando archivos específicos de librerías en la carpeta 'lib'...")
for lib in lib_files:
    src_path = os.path.join(os.getcwd(), lib)
    dest_path = os.path.join(lib_path, os.path.basename(lib))
    try:
        if os.path.isdir(src_path):  # Verifica si es una carpeta
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            print(f"Carpeta {lib} copiada en 'lib'.")
        elif os.path.isfile(src_path):  # Verifica si es un archivo
            shutil.copy(src_path, dest_path)
            print(f"Archivo {lib} copiado en 'lib'.")
        else:
            print(f"Advertencia: El archivo o carpeta {lib} no se encontró en el directorio actual.")
    except Exception as e:
        print(f"Error al copiar {lib}: {e}")

# Paso 5: Copiar los archivos principales en la raíz de CIRCUITPY
print("Copiando archivos principales en la raíz de CIRCUITPY...")
for main_file in main_files:
    src_path = os.path.join(os.getcwd(), main_file)
    dest_path = os.path.join(circuitpy_drive, main_file)
    try:
        shutil.copy(src_path, dest_path)
        print(f"Archivo {main_file} copiado en la raíz de CIRCUITPY.")
    except FileNotFoundError:
        print(f"Advertencia: El archivo {main_file} no se encontró en el directorio actual.")
    except Exception as e:
        print(f"Error al copiar {main_file}: {e}")

print("Proceso completado exitosamente.")
