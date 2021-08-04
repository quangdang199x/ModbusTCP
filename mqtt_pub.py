import paho.mqtt.client as paho
import sys
import ModbusTCP
# import Example

client = paho.Client()
if client.connect("localhost", 1883,  60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)

client.publish("test/status", ModbusTCP.currentPhaseA, 0)
client.publish("test/status", ModbusTCP.currentPhaseB, 0)

client.disconnect()
# print(ModbusTCP.currentPhaseA)
