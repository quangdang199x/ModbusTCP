import yaml
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

#Read inputs.yml files:
def readFile(filePath = None):
    with open(filePath) as fileOpended:
        data = yaml.safe_load(fileOpended)
    return data

file = readFile(filePath="inputs.yml")
devices = file["devices"]

for device in devices:
    serialNumber = device['id'].split('-', 1)[1]
    getIP = device['params']['ip']
    getPort = device['params']['port']
    getModbusID = device['params']["modbusUnitId"]
    client = ModbusClient(getIP,getPort)
    connect = client.connect()
    request = client.read_holding_registers(address=None, count=None, unit = getModbusID)
    result = request.registers
    decoder = BinaryPayloadDecoder.fromRegisters(result, Endian.Big)
    snRegisters = decoder.decode_string(20).decode("utf-8")
    if snRegisters == serialNumber:
        print(f"Serial number is the same (SN: {serialNumber})")
    elif snRegisters != serialNumber:
        print(f"IP: {getIP}. Need to change input serial number from {serialNumber} to {snRegisters}")
    client.close()