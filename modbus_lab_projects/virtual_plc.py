import os
import threading
import time
import random

from pymodbus.server import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext
)

# =====================================================================
# INDUSTRIAL REGISTER MAPPING (Holding Registers)
# HR1 (Address 1) = Tank Level (%)
# HR2 (Address 2) = Temperature x10 (°C)
# HR3 (Address 3) = Valve Status (0=Closed, 1=Open)
# =====================================================================

# Use an explicit block initializer for clean address allocation
# Address starts at 1, with a base array of [Level, Temp, Valve]
initial_data_block = ModbusSequentialDataBlock(1, [50, 300, 0])

store = ModbusSlaveContext(hr=initial_data_block)
context = ModbusServerContext(slaves=store, single=True)

def tank_process():
    level = 50
    valve = 0

    print("[SYSTEM] Process simulation thread initialized.")

    while True:
        # 1. PLC Control Hysteresis Logic
        if level >= 90:
            valve = 1
        elif level <= 30:
            valve = 0

        # 2. Tank Physics Simulation
        if valve == 0:
            level += 2
        else:
            level -= 2

        # Simulate small ambient thermal variations
        temperature = 300 + random.randint(0, 5)

        # 3. Thread-Safe Register Updates
        # Using context[0] directly interacts with the server data context safely
        # Function code '3' targets Holding Registers
        # We update all 3 consecutive registers in a single block operation
        context[0].setValues(3, 1, [level, temperature, valve])

        print(
            f"[LIVE DATA] Level={level}% | "
            f"Temp={temperature/10:.1f}°C | "
            f"Valve={'OPEN' if valve == 1 else 'CLOSED'}"
        )

        time.sleep(2)

# Start the process automation loop as a safe background worker
thread = threading.Thread(target=tank_process, daemon=True)
thread.start()

print("==================================================")
print("             VIRTUAL PLC SERVER ONLINE            ")
print("==================================================")

# =====================================================================
# DEVOPS PORTABILITY CONFIGURATION
# Bind to 0.0.0.0 so the server can bridge seamlessly out of Docker containers
# =====================================================================
BIND_IP = os.environ.get("PLC_BIND_IP", "0.0.0.0")
BIND_PORT = int(os.environ.get("PLC_BIND_PORT", 5020))

print(f"[NET] Modbus TCP Listening on: {BIND_IP}:{BIND_PORT}\n")

StartTcpServer(
    context=context, 
    address=(BIND_IP, BIND_PORT)
)