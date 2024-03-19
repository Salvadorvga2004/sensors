from machine import Pin, PWM, SoftI2C
import ssd1306
from time import sleep
import network
from umqtt.simple import MQTTClient

green_pin = 15
blue_pin = 4
red_pin = 16

i2c = SoftI2C(sda=Pin(13), scl=Pin(12))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

green_pwm = PWM(Pin(green_pin), freq=5000)
blue_pwm = PWM(Pin(blue_pin), freq=5000)
red_pwm = PWM(Pin(red_pin), freq=5000)

MQTT_BROKER = "192.168.232.79"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/svc/ky-016"
MQTT_PORT = 1883

def llegada_mensaje(topic, msg):
    print("Mensaje recibido:", msg)

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID,
                        MQTT_BROKER, 
                        user=MQTT_USER,
                        password=MQTT_PASSWORD)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, en el topico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

# Función para conectar a la red WiFi
def conectar_wifi():
    print("Conectando a WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('ElGerasxd', 'xdpapi23')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.1)
    print("  Connected!  ")

def mostrar_color(color):
    display.fill(0)
    display.text(color, 0, 0)
    display.show()

colores = [
    {"nombre": "Rojo", "green": 0, "blue": 0, "red": 1023},
    {"nombre": "Blanco", "green": 1023, "blue": 1023, "red": 1023},
    {"nombre": "Verde", "green": 1023, "blue": 0, "red": 0},
    {"nombre": "Azul", "green": 0, "blue": 1023, "red": 0}
]

conectar_wifi()
client = subscribir()

while True:
    for color in colores:

        green_pwm.duty(color["green"])
        blue_pwm.duty(color["blue"])
        red_pwm.duty(color["red"])

        mostrar_color(color["nombre"])
        
        msg = color["nombre"]
        client.publish(MQTT_TOPIC, msg)
        sleep(10)

