import yaml
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

if __name__ == "__main__":
    filePath = input()
    fix = lost = 0
    logging.basicConfig(filename="runtime.log", filemode="w", level=logging.DEBUG)
    #Read inputs.yml files:
    def readFile(filePath = None):
        try:
            with open(filePath) as fileOpended:
                data = yaml.safe_load(fileOpended)
            return data
        except Exception as e:
            logging.warning("Can't open the inputs.yml file.")
            logging.warning(e)
            exit()
    file = readFile(filePath=filePath)
    devices = file["devices"]
    #Loop for checking data:
    for device in devices:
        if device["type"] == "inverter":
            serialNumber = device['id'].split('-', 1)[1]
            getIP = device['params']['ip']
            getPort = device['params']['port']
            getModbusID = device['params']['modbusUnitId']
            getModel = device['model']
            if getModel == "PVS100":
                address = 40052
                dataType = "STR128"
            elif getModel == "STP110":
                address = 40052
                dataType = "STR16"
            elif getModel == "SHP75":
                address = 40052
                dataType = "STR32"
            elif getModel == "STP50":
                address = 30057
                dataType = "U32"
            else:
                logging.info("No type of inverter '{}' in list.".format(getModel))
            if dataType == "STR16":
                lenData = 1
            elif dataType == "STR32" or dataType == "U32":
                lenData = 2
            elif dataType == "STR64":
                lenData = 4
            elif dataType == "STR128":
                lenData = 8

            client = ModbusClient(getIP,getPort)
            connect = client.connect()
            if connect == True:
                request = client.read_holding_registers(address=address, count=lenData, unit = getModbusID)
                result = request.registers
                decoder = BinaryPayloadDecoder.fromRegisters(result, Endian.Big)
                if dataType == "STR16" or dataType == "STR32" or dataType == "STR64" or dataType == "STR128":
                    snRegisters = decoder.decode_string(len(serialNumber)).decode("utf-8")
                elif dataType == "U32":
                    snRegistersTemp = decoder.decode_32bit_uint()
                    snRegisters = str(snRegistersTemp)
                if snRegisters == serialNumber:
                    logging.debug("Serial number '{}' is correct.".format(serialNumber))
                    # print(f"Serial number {serialNumber} is the same")
                elif snRegisters != serialNumber:
                    logging.debug("IP: '{}' ModbusUnitID: {}. Need to change input serial number from '{}' to '{}'".format(getIP, getModbusID, serialNumber, snRegisters))
                    fix += 1
                    # print(f"IP: {getIP} ModbusUnitID: {getModbusID}. Need to change input serial number from {serialNumber} to {snRegisters}")
                client.close()
            elif connect == False:
                logging.error("Connection to ('{}', {}) failed.".format(getIP, getPort))
                lost += 1
                # print(f"No connection to IP: {getIP}")
        else:
            pass
    logging.debug("Finish checking the serial number. Need to fix: {} serial number.".format(fix))
    logging.debug("No connection: {}".format(lost))
    exit()
