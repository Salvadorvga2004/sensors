from machine import Pin, ADC
from time import sleep
import network
from umqtt.simple import MQTTClient

KY026a = 34
LED = 13
KY026d = 15

adc = ADC(Pin(KY026a))
adc.width(ADC.WIDTH_10BIT)
adc.atten(ADC.ATTN_11DB)

led = Pin(LED, Pin.OUT)
digital_sensor = Pin(KY026d, Pin.IN)

MQTT_BROKER = "192.168.232.79"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/svc/ky-026"
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
    sta_if.connect('ElGerasxd', 'xdpapi23')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.1)
    print("  Connected!  ")

conectar_wifi()
client = subscribir()

while True:
    valor = digital_sensor.value()
    print(valor)
        
    if valor == 1:
        msg = b'true'
        print("Fuego!!!")
        led.on()
    elif valor == 0:
        msg = b'false'
        print("Seguro")
        led.off()
    
    client.publish(MQTT_TOPIC, msg)
    sleep(15)