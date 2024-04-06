from machine import Pin
from time import sleep
import network
from umqtt.simple import MQTTClient

relay_pin = 12
relay = Pin(relay_pin, Pin.OUT)

MQTT_BROKER = "192.168.232.79"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/svc/ky-019"
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
        relay.value(1)
        sleep(3)
    if msg == b'false':
        relay.value(0)
        sleep(3)


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