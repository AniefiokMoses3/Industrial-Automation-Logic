import os
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# =====================================================================
# DEVOPS & TELEMETRY CONFIGURATION
# Allow environment variables to dynamically point to the server target
# Default to localhost for easy manual testing
# =====================================================================
PLC_IP = os.environ.get("PLC_IP", "127.0.0.1")
PLC_PORT = int(os.environ.get("PLC_PORT", 5020))
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", 2)) # Throttling control

print("==================================================")
print(f"        SCADA CLIENT ONLINE (Target: {PLC_IP}:{PLC_PORT})")
print("==================================================")

# Initialize the persistent client object using modern 3.6.9 syntax
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

while True:
    # 1. Resilient Connection Guard
    if not client.connected:
        print("[CONNECTING] Attempting handshake with Modbus server...")
        success = client.connect()
        if not success:
            print("[RETRY] Connection failed. Remote server may be offline. Retrying in 5 seconds...")
            time.sleep(5)
            continue
        else:
            print("[SUCCESS] Connected to industrial data stream.")

    # 2. Secure Data Acquisition Layer
    try:
        # Polling 3 consecutive registers starting at address 1
        result = client.read_holding_registers(address=1, count=3, slave=1)

        # 3. Modbus Level Error Check (e.g., Illegal Data Address or Exception codes)
        if result.isError():
            print(f"[ALARM] Modbus Protocol Error encountered: {result}")
        else:
            # Safely unpack data payload
            level = result.registers[0]
            temp = result.registers[1] / 10
            valve = result.registers[2]

            print(
                f"[DATA] Level={level:3d}% | "
                f"Temp={temp:5.1f}°C | "
                f"Valve={'OPEN' if valve else 'CLOSED'}"
            )

    except (ModbusException, Exception) as e:
        # Catch unexpected physical drops, socket timeouts, or network crashes
        print(f"[NETWORK ERROR] Connection lost or packet broken: {e}")
        print("[SYSTEM] Forcing client state reset for clean recovery...")
        client.close()  # Close the broken socket gracefully down to avoid resource leaks

    # 4. Process Throttle (Prevents resource exhaustion)
    time.sleep(POLL_INTERVAL)