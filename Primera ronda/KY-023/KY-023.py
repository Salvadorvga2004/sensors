from machine import Pin, ADC, SoftI2C
from time import sleep 
import ssd1306

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

sw = ADC(Pin(34))
vrx = ADC(Pin(35))
vry = ADC(Pin(33))

vrx.atten(ADC.ATTN_11DB)
vry.atten(ADC.ATTN_11DB)

vrx.width(ADC.WIDTH_12BIT)
vry.width(ADC.WIDTH_12BIT)

while True:
    valorx = vrx.read()
    print(valorx)
    valory = vry.read()
    print(valory)

    display.fill(0)
    display.text('X: {}'.format(valorx), 0, 0)
    display.text('Y: {}'.format(valory), 0, 20)
    display.show()
    sleep(1)
