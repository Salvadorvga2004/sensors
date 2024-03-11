from machine import Pin
from time import sleep
import network
from umqtt.simple import MQTTClient

pinLED = 15
pinMicrophone = 33

led = Pin(pinLED, Pin.OUT)
microphone = Pin(pinMicrophone, Pin.IN)

MQTT_BROKER = "broker.hivemq.com"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/svc/ky-038"
MQTT_PORT = 1883

def llegada_mensaje(topic, msg):
    print("Mensaje recibido:", msg)

def subscribir():
    client = MQTTClient(MQTT_CLIENT_ID,
                        MQTT_BROKER, 
                        user=MQTT_USER,
                        password=MQTT_PASSWORD)
    client.set_callback(llegada_mensaje)  # Configurar la función de devolución de llamada
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, en el topico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

# Función para conectar a la red WiFi
def conectar_wifi():
    print("Conectando a WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Red', '12345678')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.1)
    print("  Connected!  ")

conectar_wifi()
client = subscribir()

while True:
    soundDetected = microphone.value()
    if soundDetected:
        led.value(1)
        msg = b'true'
        print ("Encendido")
        sleep(1)
    else:
        led.value(0)
        msg = b'false'
        print ("Apagado")
    
    client.publish(MQTT_TOPIC, msg)
    sleep(15)




