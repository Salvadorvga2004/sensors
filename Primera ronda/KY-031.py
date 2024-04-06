from machine import Pin, SoftI2C
import ssd1306
import time

hit_pin = 33

i2c= SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

hit = Pin(hit_pin, Pin.IN)

while True:
    valor = hit.value()

    if valor == 1:
        display.fill(0)
        display.text("Aguas!!!!", 0, 0)
        display.show()
        time.sleep(2)
        
   
    else:
        display.fill(0)
        display.text("Inactivo", 0, 0)
        display.show()
        time.sleep(2)
        
