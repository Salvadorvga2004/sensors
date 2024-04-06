from machine import Pin, SoftI2C
from time import sleep
import ssd1306
import dht

# Configurar el sensor DHT11 en el pin 15
sensor = dht.DHT11(Pin(15))

# Inicializar la interfaz I2C y la pantalla OLED
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    # Realizar una lectura del sensor
    sensor.measure()
    # Obtener la temperatura y la humedad
    temperatura = sensor.temperature()
    humedad = sensor.humidity()

    # Limpiar la pantalla OLED
    display.fill(0)
    # Mostrar los valores de temperatura y humedad en la pantalla OLED
    display.text('Temperatura: %d C' % temperatura, 0, 0,6)
    display.text('Humedad: %d %%' % humedad, 0, 20)
    display.show()

    # Esperar un tiempo antes de la próxima lectura
    sleep(2)
