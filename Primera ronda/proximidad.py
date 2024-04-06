from machine import Pin, SoftI2C
from time import sleep
import ssd1306
from hcsr04 import HCSR04

#Declaramos un objeto con los pines utilizados 
#para la interfaz I2C
i2c= SoftI2C(sda=Pin(21), scl=Pin(22))

#Declaramos un objeto del tipo display
display = ssd1306.SSD1306_I2C(128,64,i2c)

#DEclaramos el objeto sensor
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=24000)

#Contador
count = 0

while True:
  #Lo que hace la linea siguiente es que limpia la pantalla

  distancia = sensor.distance_cm()
  sleep(1)

  display.fill(0)
  count+=1
  display.text(str(distancia), 0,0,6)
  display.show()
  sleep(1)