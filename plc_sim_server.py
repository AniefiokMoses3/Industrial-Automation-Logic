import logging
import time
import threading
import random
import inspect
import asyncio
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusDeviceContext, ModbusServerContext

# 1. System Logging Configuration
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.ERROR)  # Keeps terminal clean from network spam

# 2. Memory Rack Initialization
# We start our block explicitly at Address 1.
# It holds 3 values: [Tank Level, Temperature, Valve Status]
initial_values = [50, 300, 1]
store_block = ModbusSequentialDataBlock(1, initial_values)
#print(store_block.simdata)
#print(type(store_block))

#for item in sorted(dir(store_block)):
#    if not item.startswith("_"):
#        print(item)
store = ModbusDeviceContext(hr=store_block)
context = ModbusServerContext(devices=store, single=True)


# 3. Tank Physics Simulation Worker
def tank_physics_simulator():
    """Simulates background tank changes by updating the exact memory blocks."""
    print("🚀 [PHYSICS ENGINE] Tank simulation background thread active.")
    current_level = 50
    direction = 1  # 1 = Filling, -1 = Draining

    while True:
        # Step the tank level up or down
        current_level += (2 * direction)
        
        # High/Low Boundary Safety Rules
        if current_level >= 90:
            direction = -1
            print("\n⚠️ [ALARM] High-level threshold (90%). Opening discharge valve...")
            # Address 3 is our Valve Status register
            store_block.simdata[0].values[2] = 1 
        elif current_level <= 30:
            direction = 1
            print("\n⚠️ [ALARM] Low-level threshold (30%). Closing discharge valve...")
            store_block.simdata[0].values[2] = 0

        # Write updated values back to the sequential memory blocks
        # Address 1: Tank Level
        store_block.simdata[0].values[0] = current_level
        
        # Address 2: Temperature (Fluctuating slightly around 30.0C)
        sim_temp = 300 + random.randint(0, 5)
        store_block.simdata[0].values[1] = sim_temp
        print(
            f"Level = {current_level},"
            f"Tem = {sim_temp},"
            f"Direction = {direction}"
        )

        time.sleep(2)  # Wait 2 seconds before the next physical shift

# Initialize and launch the background daemon thread
simulation_thread = threading.Thread(target=tank_physics_simulator, daemon=True)
simulation_thread.start()

# 4. Network Gateway Deployment
LOCAL_IP = "127.0.0.1"
LOCAL_PORT = 5020

print("=============================================")
print("      VIRTUAL PLC TANK SIMULATION ENGINE     ")
print("=============================================")
print(f"📡 Modbus/TCP Gateway Online at {LOCAL_IP}:{LOCAL_PORT}")
print("Waiting for SCADA client telemetry polls...\n")

async def test_context():
    for addr in range(0, 5):
        result = await context.async_getValues(
            device_id=1,
            func_code=3,
            address=addr,
            count=1
        )
        print(f"Address {addr} -> {result}")

asyncio.run(test_context())   

StartTcpServer(context=context, address=(LOCAL_IP, LOCAL_PORT))