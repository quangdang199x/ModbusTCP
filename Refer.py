idx = 0
fCheckSN = False

log.debug('Check Serial Number from input file and device')
for device in devices:
    #Read serialNumber from device
    devSerialNumberRead = read_devSN(device)

    #Read serialNumber from inputs.yml
    inputs_file = 'configs/inputs.yml'
    try:
        with open(inputs_file) as opened_file:
            configs = yaml.safe_load(opened_file)
            device = configs['devices'][idx]
        devSerialNumberInput = device['id'].split('-')[1]
    except Exception as e:
        log.warning('Failed to load device serial number.')
        log.warning(e)
    if devSerialNumberInput == devSerialNumberRead :
        log.debug('Input SN from {} is correct.'.format(devSerialNumberInput))
        fCheckSN = fCheckSN and True
    else:
        log.debug('Need to change input SN from {} to {}'.format(devSerialNumberInput, devSerialNumberRead))

    idx = idx + 1
if ! fCheckSN :
    return
else:
    log.debug('Finish checking the serial number')
