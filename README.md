TÌM HIỂU GIAO THỨC TRUYỀN THÔNG MODBUS TCP/IP

# -------------------------------------------------------- 
# I. Đọc 1 Inverter giả lập bằng Modbus TCP, sử dụng thư viện pymodbus:

[
import pymodbus
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
from twisted.internet.defer import Deferred
client = ModbusClient(host="127.0.0.1", port=502)
conection = client.connect()
class ScaleFactor:
    GAIN0 = 1
    GAIN1 = 10
    GAIN2 = 100
    GAIN3 = 1000
    FIX0 = 1
    FIX1 = 0.1
    FIX2 = 0.01
    FIX3 = 0.001
def myRegisters():
    result = client.read_holding_registers(40001, 50, unit = 1)
    currentPhaseA = (result.registers[0] << 16 | result.registers[1])*ScaleFactor.FIX3
    currentPhaseB = (result.registers[2] << 16 | result.registers[3])*ScaleFactor.FIX3
    currentPhaseC = (result.registers[4] << 16 | result.registers[5])*ScaleFactor.FIX3
    powerPhaseA = (result.registers[6] << 16 | result.registers[7])*ScaleFactor.FIX0
    powerPhaseB = (result.registers[8] << 16 | result.registers[9])*ScaleFactor.FIX0
    powerPhaseC = (result.registers[10] << 16 | result.registers[11])*ScaleFactor.FIX0
    voltagePhaseA = (result.registers[12] << 16 | result.registers[13])*ScaleFactor.FIX2
    voltagePhaseB = (result.registers[14] << 16 | result.registers[15])*ScaleFactor.FIX2
    voltagePhaseC = (result.registers[16] << 16 | result.registers[17])*ScaleFactor.FIX2
    frequency = result.registers[18]*ScaleFactor.FIX2
    totalYield = ((result.registers[19] << 16 | result.registers[20]) << 32 | (result.registers[21] << 16 | result.registers[22]))*ScaleFactor.FIX0
    dailyYield = ((result.registers[23] << 16 | result.registers[24]) << 32 | (result.registers[25] << 16 | result.registers[26]))*ScaleFactor.FIX0
    operatingTime = ((result.registers[27] << 16 | result.registers[28]) << 32 | (result.registers[29] << 16 | result.registers[30]))*ScaleFactor.FIX0
    mpptCurrent1 = (result.registers[31] << 16 | result.registers[32])*ScaleFactor.FIX3
    mpptVoltage1 = (result.registers[33] << 16 | result.registers[34])*ScaleFactor.FIX2
    mpptPower1 = (result.registers[35] << 16 | result.registers[36])*ScaleFactor.FIX0
    print("currentPhaseA: %sA" %currentPhaseA)
    print("currentPhaseB: %sA" %currentPhaseB)
    print("currentPhaseC: %sA" %currentPhaseC)
    print("powerPhaseA: %sW" %powerPhaseA)
    print("powerPhaseB: %sW" %powerPhaseB)
    print("powerPhaseC: %sW" %powerPhaseC)
    print("voltagePhaseA: %sV" %voltagePhaseA)
    print("voltagePhaseB: %sV" %voltagePhaseB)
    print("voltagePhaseC: %sV" %voltagePhaseC)
    print("frequency: %sHz" %frequency)
    print("totalYield: %sWh" %totalYield)
    print("dailyYield: %sWh" %dailyYield)
    print("operatingTime: %ss" %operatingTime)
    print("mpptCurrent1: %sA" %mpptCurrent1)
    print("mpptVoltage1: %sV" %mpptVoltage1)
    print("mpptPower1: %sW" %mpptPower1)
while True:
    myRegisters()
    print("\n")
    time.sleep(10)
]

####=> Kết quả mô phỏng:
currentPhaseA: 13.775A
currentPhaseB: 11.411A
currentPhaseC: 12.558A
powerPhaseA: 8977W    
powerPhaseB: 9872W
powerPhaseC: 9784W
voltagePhaseA: 225.55V
voltagePhaseB: 225.78V
voltagePhaseC: 234.65V
frequency: 49.54Hz
totalYield: 47528532Wh
dailyYield: 43538Wh
operatingTime: 8555139s
mpptCurrent1: 5.372A
mpptVoltage1: 733.42V
mpptPower1: 3986W


# -----------------------------------------------------------
# II. Lưu dữ liệu vào Influxdb và hiển thị dữ liệu lên Grafana:
#Cài đặt thư viện:
#pip install influxdb
#Phần code:
[
from dateutil.parser import DEFAULTPARSER
from pymodbus import payload
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
from twisted.internet.defer import Deferred
import json
from influxdb import InfluxDBClient, client
from datetime import datetime
#Setup database:
client_1 = ModbusClient(host="127.0.0.1", port=502)
conection = client_1.connect()
print(conection) #Check connection.
client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'mydb')
client.create_database('mynewdb')
client.get_list_database()
client.switch_database('mynewdb')
class ScaleFactor:
    GAIN0 = 1
    GAIN1 = 10
    GAIN2 = 100
    GAIN3 = 1000
    FIX0 = 1
    FIX1 = 0.1
    FIX2 = 0.01
    FIX3 = 0.001
    pass
def myField():
    result = client_1.read_holding_registers(40001, 50, unit = 1)
    currentPhaseA = (result.registers[0] << 16 | result.registers[1])*ScaleFactor.FIX3
    currentPhaseB = (result.registers[2] << 16 | result.registers[3])*ScaleFactor.FIX3
    currentPhaseC = (result.registers[4] << 16 | result.registers[5])*ScaleFactor.FIX3
    powerPhaseA = (result.registers[6] << 16 | result.registers[7])*ScaleFactor.FIX0
    powerPhaseB = (result.registers[8] << 16 | result.registers[9])*ScaleFactor.FIX0
    powerPhaseC = (result.registers[10] << 16 | result.registers[11])*ScaleFactor.FIX0
    voltagePhaseA = (result.registers[12] << 16 | result.registers[13])*ScaleFactor.FIX2
    voltagePhaseB = (result.registers[14] << 16 | result.registers[15])*ScaleFactor.FIX2
    voltagePhaseC = (result.registers[16] << 16 | result.registers[17])*ScaleFactor.FIX2
    frequency = result.registers[18]*ScaleFactor.FIX2
    totalYield = ((result.registers[19] << 16 | result.registers[20]) << 32 | (result.registers[21] << 16 | result.registers[22]))*ScaleFactor.FIX0
    dailyYield = ((result.registers[23] << 16 | result.registers[24]) << 32 | (result.registers[25] << 16 | result.registers[26]))*ScaleFactor.FIX0
    operatingTime = ((result.registers[27] << 16 | result.registers[28]) << 32 | (result.registers[29] << 16 | result.registers[30]))*ScaleFactor.FIX0
    mpptCurrent1 = (result.registers[31] << 16 | result.registers[32])*ScaleFactor.FIX3
    mpptVoltage1 = (result.registers[33] << 16 | result.registers[34])*ScaleFactor.FIX2
    mpptPower1 = (result.registers[35] << 16 | result.registers[36])*ScaleFactor.FIX0
    #Setup Payload:
    json_payload = []
    current_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data = {
        "measurement"  : "Inverter_1",
        "tags" : {},
        "time" : current_time,
        "fields" : {
            "currentPhaseA" : currentPhaseA, 
            "currentPhaseB" : currentPhaseB, 
            "currentPhaseC" : currentPhaseC, 
            "powerPhaseA" : powerPhaseA, 
            "powerPhaseB" : powerPhaseB, 
            "powerPhaseC" : powerPhaseC, 
            "voltagePhaseA" : voltagePhaseA, 
            "voltagePhaseB" : voltagePhaseB, 
            "voltagePhaseC" : voltagePhaseC, 
            "frequency" : frequency, 
            "totalYield" : totalYield, 
            "dailyYield" : dailyYield, 
            "operatingTime" : operatingTime, 
            "mpptCurrent1" : mpptCurrent1, 
            "mpptVoltage1" : mpptVoltage1, 
            "mpptPower1" : mpptPower1 
        }
    }
    json_payload.append(data)

    #Send my payload:
    client.write_points(json_payload)
    myPayload = client.query('select * from Inverter_1;')
    print("Running")
while True:
    myField()
    time.sleep(5)
]

####=> Kết quả mô phỏng cho 1 payload:
C:\Users\phamd\OneDrive\Máy tính\Study\Modbus_TCP-RTU-main\Modbus_TCP-RTU-main>python Example.py
ResultSet({'('Inverter_1', None)': [{'time': '2021-07-26T09:59:13Z', 'currentPhaseA': 35.536, 'currentPhaseB': 50.433, 'currentPhaseC': 46.982, 'dailyYield': 48263, 'frequency': 48.99, 'mpptCurrent1': 5.372, 'mpptPower1': 3986, 'mpptVoltage1': 733.42, 'operatingTime': 8578792, 'powerPhaseA': 8342, 'powerPhaseB': 7569, 'powerPhaseC': 8623, 'totalYield': 47552185, 'voltagePhaseA': 236.15, 'voltagePhaseB': 237.05, 'voltagePhaseC': 238.07}]})


# -------------------------------------------------------------------------
# III. Sử dụng MQTT để public dữ liệu lên localhost và subscribe dữ liệu từ localhost về:
#cài đặt thư viện: pip install paho-mqtt
#cài đặt mosquitto về máy

#Phần code cho mqtt public:
[
import time
import paho.mqtt.client as paho
import sys
import ModbusTCP
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
]

####=> Kết quả public dữ liệu lên localhost:
PS C:\Program Files\Mosquitto> ./mosquitto_sub -t value
currentPhaseA: 15.052A
currentPhaseB: 12.688A
currentPhaseC: 13.835A
voltagePhaseA: 238.32V
voltagePhaseB: 238.55V
voltagePhaseC: 247.42000000000002V
powerPhaseA: 10254W
powerPhaseB: 11149W
powerPhaseC: 11061W
frequency: 49.54Hz
dailyEnergy: 44815Wh
totalEnergy: 47529809Wh
operatingTime: 8556416s
mpptCurrent1: 5.372A
mpptVoltage1: 733.42V
mpptPower1: 3986W

#Phần code cho mqtt subscribe:
[
import paho.mqtt.client as paho
import sys
def onMessage(client, userdata, msg):
    print(msg.topic +": " + msg.payload.decode())
client = paho.Client()
client.on_message = onMessage
if client.connect("localhost", 1883,  60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)
client.subscribe("value")
try: 
    print("Connecting...")
    client.loop_forever()
except:
    print("Disconnecting from Broker")

client.disconnect()
]

####=> Kết quả subscribe dữ liệu từ localhost về:
C:\Users\phamd\OneDrive\Máy tính\Study\Modbus_TCP-RTU-main\Modbus_TCP-RTU-main>python mqtt_sub.py
Connecting...
value: currentPhaseA: 15.294A
value: currentPhaseB: 12.93A
value: currentPhaseC: 14.077A
value: voltagePhaseA: 240.74V
value: voltagePhaseB: 240.97V
value: voltagePhaseC: 249.84V
value: powerPhaseA: 10496W
value: powerPhaseB: 11391W
value: powerPhaseC: 11303W
value: frequency: 49.54Hz
value: dailyEnergy: 45057Wh
value: totalEnergy: 47530051Wh
value: operatingTime: 8556658s
value: mpptCurrent1: 5.372A
value: mpptVoltage1: 733.42V
value: mpptPower1: 3986W
value: