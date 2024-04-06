from machine import Pin, SoftI2C
import ssd1306

led_pin = 33
sensor_pin = 32

i2c= SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

led = Pin(led_pin, Pin.OUT)
sensor = Pin(sensor_pin, Pin.IN)
sensor.init(Pin.IN, Pin.PULL_UP)

while True:
    val = sensor.value()

    if val == 1:
        led.value(0)
        display.fill(0)
        display.text("Apagado", 0, 0)
        display.show()
    else:
        led.value(1)
        display.fill(0)
        display.text("Encendido", 0, 0)
        display.show()
