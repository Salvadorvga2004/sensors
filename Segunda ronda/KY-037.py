from machine import Pin, ADC
from time import sleep
import network
from umqtt.simple import MQTTClient

MQTT_BROKER = "broker.hivemq.com"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/svc/ky-037"
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

led_pin = 15
sound_analog_pin = 33

led = Pin(led_pin, Pin.OUT)
adc = ADC(Pin(sound_analog_pin), atten=ADC.ATTN_11DB)

while True:
    val_analog = adc.read()
    if val_analog > 200:
        msg = b'true'
        print(val_analog)
        led.value(1)
    else:
        msg = b'false'
        print(val_analog)
        led.value(0)
    
    client.publish(MQTT_TOPIC, msg)
    sleep(10)
