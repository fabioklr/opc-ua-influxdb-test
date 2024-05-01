# OPC UA and InfluxDB Test

This is a simple test to show how to connect an OPC UA server to an InfluxDB database. The server is written in Python and uses the `asnycua` and `influxdb3-client` libraries. The server sends out 3 values every five seconds from a real data set when it gets started. It is intended for testing and illustration purposes.

## Overview
This projects consists of three parts:
1. OPC UA Server: This element simulates a sensor and sends out data on three variables - temperature, pressure and a setting.
2. Broker: This element is a simple OPC UA client that retrieves data from the server and sends it to the InfluxDB database.
3. InfluxDB: This is a time-series database that stores the data sent by the broker.

![Blueprint](Blueprint.png)

## IT
The OPC UA Server is a Docker container on a VM in the Akamai Cloud. The broker is another Docker container on the same VM. The InfluxDB is a managed service on Azure, accessible through Influxdata's web app.
