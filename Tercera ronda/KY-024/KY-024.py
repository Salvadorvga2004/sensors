from machine import Pin, ADC, SoftI2C
import ssd1306
from time import sleep
import network
from umqtt.simple import MQTTClient

Led = Pin(15, Pin.OUT)
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)

i2c= SoftI2C(sda=Pin(15), scl=Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

MQTT_BROKER = "192.168.232.79"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/svc/ky-024"
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
    val = adc.read()
    
    if val > 3000:
        Led.value(1)
        msg = b'true'
        display.fill(0)
        display.text("Detectado", 0, 0)
        display.show()
    else:
        Led.value(0)
        msg = b'false'
        display.fill(0)
        display.text("No detectado", 0, 0)
        display.show()
    client.publish(MQTT_TOPIC, msg)
    sleep(10)

