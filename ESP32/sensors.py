# test BH1750

import machine
#import BH1750
import time
import MCP9808

#i2c = machine.I2C(scl = machine.Pin(22), sda = machine.Pin(21), freq=400000)
i2c = machine.I2C(scl = machine.Pin(22), sda = machine.Pin(21))

# BH1750
# while True:
#   print(BH1750.sample(i2c))

# MCP9808
mcp = MCP9808.MCP9808(i2c=i2c)
mcp.set_resolution(MCP9808.T_RES_MAX)
while True:
	print("temp: {0}°C".format(mcp.get_temp()))
	time.sleep(1)
