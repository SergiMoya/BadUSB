# **BadUSB - Configuración y Personalización con PicoDucky (Waveshare RP2040-One)**
Este repositorio permite configurar un **BadUSB** utilizando el microcontrolador **RP2040**, concretamente el dispositivo **Waveshare RP2040-One** y la herramienta **PicoDucky**. El objetivo es automatizar la configuración y modificación de los comandos payload mediante DuckyScript.

## **Descripción del proceso**

### **1. Inicialización del dispositivo:**
---
Para comenzar, asegúrate de mantener presionado el botón de BOOT mientras conectas el dispositivo USB al ordenador. Esto pondrá el dispositivo en modo de configuración.



### **2. Ejecutar el script de configuración:**
---
Una vez el dispositivo esté conectado, navega a la carpeta config-usb y ejecuta el siguiente comando en tu terminal o consola de comandos:

<u>python RECONFIGURAR.py</u>

### **3. Configuración del USB:**
---
El script te pedirá que ingreses la letra de la unidad USB conectada. Ingresa la letra (sin los dos puntos) y presiona Enter. Luego, espera unos segundos para que el proceso de configuración se complete.

### **4. Modificar el payload:**
---
Una vez que el dispositivo se haya configurado correctamente, podrás modificar el archivo payload.dd utilizando Ducky Script para personalizar los comandos que deseas ejecutar en el dispositivo.

### **5. Desconectar el dispositivo:**
---
Al finalizar la configuración, simplemente retira el USB de manera segura.

### **Funcionamiento posterior**
---
La próxima vez que conectes el BadUSB (sin presionar el botón BOOT), el dispositivo ejecutará automáticamente los comandos asignados en el archivo payload.dd sin necesidad de intervención adicional.

### **Nota importante:**
Al conectar el dispositivo sin presionar el botón BOOT, será reconocido por el sistema como un teclado DELL en español
