from machine import Pin, PWM, SoftI2C
import ssd1306
import time

green_pin = 25
blue_pin = 33
red_pin = 32

i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

green_pwm = PWM(Pin(green_pin), freq=5000)
blue_pwm = PWM(Pin(blue_pin), freq=5000)
red_pwm = PWM(Pin(red_pin), freq=5000)

def mostrar_color(color):
    display.fill(0)
    display.text(color, 0, 0)
    display.show()

colores = [
    {"nombre": "Verde", "green": 0, "blue": 0, "red": 1023},
    {"nombre": "Blanco", "green": 1023, "blue": 1023, "red": 1023},
    {"nombre": "Rojo", "green": 1023, "blue": 0, "red": 0},
    {"nombre": "Azul", "green": 0, "blue": 1023, "red": 0}
]

while True:
    for color in colores:

        green_pwm.duty(color["green"])
        blue_pwm.duty(color["blue"])
        red_pwm.duty(color["red"])

        mostrar_color(color["nombre"])

        time.sleep(2)
