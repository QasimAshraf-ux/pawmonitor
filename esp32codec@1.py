# IMPORTS
import network
import time
from machine import Pin, ADC
from time import sleep
from umqtt.simple import MQTTClient
# WIFI CREDENTIALS
ssid = "Arabica"
password = "Stardust@147X"
# CONNECTION TO WIFI
def connect():
    wifi = network.WLAN(network.STA_IF) # assigns a "wifi" identifier to the hardware of the esp32
    wifi.active(True) # switches on the wifi hardware of the micro-controller
    wifi.connect(ssid, password) # attempts to connect the "wifi" to the wifi
    while not wifi.isconnected(): # run a loop that re-attempts connection in case connection isn't successful
        print(".", end="")
        time.sleep(0.5) # reattempt at 0.5s intervals
    print("\nConnected to WiFi!")
    print("IP Address: ", wifi.ifconfig()[0]) # wifi.ifconfig is a tuple of 4 elements, element 0 contains the IP address
connect()
# RELAY INFORMATION TO PI
client = MQTTClient("esp32_ashraf", "192.168.100.7")
client.connect()
# DATA READINGS
rval = ADC(Pin(32)) # determines the pin from which data is to be read
rval.atten(ADC.ATTN_11DB) # determines the range of values to be read (0 to 3.3V)
while True: # runs while connected
    sum = 0
    n = 0
    while n < 1000: # takes 1000 samples for one rms (root-mean-square value)
        rvaltrue = rval.read() # reads a value
        vval = (3.3 * rvaltrue) / 4095 # converts the raw ADC value to a voltage value
        vval = (vval - 1.65) ** 2 # removes the intended bias of 1.65V
        sum = sum + vval # sums the values taken for later calculation of rms
        n = n + 1
        sleep(0.001) # re-read at 1ms intervals
    rms = (sum * (1/n)) ** (1/2) # calculation of rms
    curS = rms / 62 # converts rms to the associated current (secondary) using burden resistance value of 62 ohms
    curP = 1800 * curS # converts secondary current to the primary mains current using the transformer (SCT-013-30A) turns ratio
    pvalnow = curP * 220 # converts mains current to the power reading, pakistan standard voltage is 220V
    client.publish("ashraf/power", str(pvalnow)) # send the value to pi
    print("value sent!")

