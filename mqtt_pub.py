import time
import paho.mqtt.client as paho
import sys
import ModbusTCP
# import Example

client = paho.Client()
if client.connect("localhost", 1883,  60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)


count = 0
while count != 10:
    print(f"Running...{count}")
    client.publish("value", ModbusTCP.currentPhaseA, 0)
    client.publish("value", ModbusTCP.currentPhaseB, 0)
    client.publish("value", ModbusTCP.currentPhaseC, 0)
    client.publish("value", ModbusTCP.voltagePhaseA, 0)
    client.publish("value", ModbusTCP.voltagePhaseB, 0)
    client.publish("value", ModbusTCP.voltagePhaseC, 0)
    client.publish("value", ModbusTCP.powerPhaseA, 0)
    client.publish("value", ModbusTCP.powerPhaseB, 0)
    client.publish("value", ModbusTCP.powerPhaseC, 0)
    client.publish("value", ModbusTCP.frequency, 0)
    client.publish("value", ModbusTCP.dailyYield, 0)
    client.publish("value", ModbusTCP.totalYield, 0)
    client.publish("value", ModbusTCP.operatingTime, 0)
    client.publish("value", ModbusTCP.mpptCurrent1, 0)
    client.publish("value", ModbusTCP.mpptVoltage1, 0)
    client.publish("value", ModbusTCP.mpptPower1, 0)
    client.publish("value", " ", 0)
    count += 1
    time.sleep(10)
    
print("Disconnected")
client.disconnect()
