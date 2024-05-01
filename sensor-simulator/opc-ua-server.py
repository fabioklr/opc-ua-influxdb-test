import logging
import asyncio
import pandas as pd
from asyncua import Server, ua

async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840')
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://devnetiot.com/opcua/'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    obj_vplc = await server.nodes.objects.add_object(idx, 'vPLC1')
    var_temperature = await obj_vplc.add_variable(idx, 'temperature', 0)
    var_pressure = await obj_vplc.add_variable(idx, 'pressure', 0)
    var_pumpsetting = await obj_vplc.add_variable(idx, 'pumpsetting', 0)

    # Read Sensor Data from Kaggle
    df = pd.read_csv("sensor.csv")
    # Only use sensor data from 03 and 01 (preference)
    sensor_data = pd.concat([df["sensor_03"], df["sensor_01"]], axis=1)

    _logger.info('Starting server!')
    async with server:
        while True:
            for row in sensor_data.itertuples():
                # if below the mean use different setting - just for testing
                if row[1] < df["sensor_03"].mean():
                    setting = "standard"
                else:
                    setting = "speed"
                _logger.info(f"Temperature: {row[1]}, Pressure: {row[2]}, Pump Setting: {setting}")
                # Writing Variables
                await var_temperature.write_value(float(row[1]))
                await var_pressure.write_value(float(row[2]))
                await var_pumpsetting.write_value(str(setting))
                await asyncio.sleep(5)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)