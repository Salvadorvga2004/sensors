from machine import Pin, SoftI2C
import ssd1306
from time import sleep
import network
from umqtt.simple import MQTTClient

i2c= SoftI2C(sda=Pin(13), scl=Pin(12))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

buzzer_pin = 15
buzzer = Pin(buzzer_pin, Pin.OUT)

MQTT_BROKER = "192.168.232.79"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/svc/ky-012"
MQTT_PORT = 1883

#Función para conectar a WiFi
def conectar_wifi():
    print("Conectando...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('ElGerasxd', 'xdpapi23')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("WiFi Conectada!")


def llegada_mensaje(topic, msg):
    print("Mensaje:", msg)
    if msg == b'true':
        display.fill(0)
        display.text("Tocando", 0, 0)
        display.show()
        buzzer.value(1)
        sleep(0.5)
        buzzer.value(0)
        sleep(0.5)
    if msg == b'false':
        display.fill(0)
        display.text("Silencio", 0, 0)
        display.show()
        buzzer.value(0)
        sleep(0.5)


def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID,
     MQTT_BROKER, port=MQTT_PORT, 
     user=MQTT_USER,
     password=MQTT_PASSWORD,
     keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, en el topico %s"%(MQTT_BROKER, MQTT_TOPIC))
    return client

conectar_wifi()

client = subscribir()


while True:
    client.wait_msg()
