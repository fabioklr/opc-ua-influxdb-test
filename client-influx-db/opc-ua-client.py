import asyncio
from asyncua import Client
import os
from influxdb_client_3 import InfluxDBClient3, Point
from dotenv import load_dotenv

load_dotenv()

influx_token = os.environ.get("INFLUXDB_TOKEN")
influx_org = "influx-test"
influx_host = "https://westeurope-1.azure.cloud2.influxdata.com"
influx_client = InfluxDBClient3(host=influx_host, token=influx_token, org=influx_org)
sensor_host_ip = os.environ.get("SENSOR_HOST_IP")
sensor_host = f"opc.tcp://{sensor_host_ip}:4840"
sensor_client = Client(sensor_host)

async def get_data():
    await sensor_client.connect()
    root = sensor_client.nodes.root
    temperature_var = await root.get_child(["0:Objects", "2:vPLC1", "2:temperature"])
    pressure_var = await root.get_child(["0:Objects", "2:vPLC1", "2:pressure"])
    pumpsetting_var = await root.get_child(["0:Objects", "2:vPLC1", "2:pumpsetting"])
    temperature = await temperature_var.read_value()
    pressure = await pressure_var.read_value()
    pumpsetting = await pumpsetting_var.read_value()
    vars = [temperature, pressure, pumpsetting]
    return vars

def write_data(variables):
    temperature = variables[0]
    pressure = variables[1]
    pumpsetting = variables[2]
    point = Point("sensors").tag("location", "vPLC1").field("temperature", temperature).field("pressure", pressure).field("pumpsetting", pumpsetting)
    influx_client.write(database="sensor-simulator-bucket", record=point)

if __name__ == "__main__":
    variables = asyncio.run(get_data())
    write_data(variables)    