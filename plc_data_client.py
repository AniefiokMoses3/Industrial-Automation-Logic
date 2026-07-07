import time
from pymodbus.client import ModbusTcpClient

# Network Configuration
PLC_IP = "127.0.0.1"
PLC_PORT = 5020

print("=============================================")
print("      SCADA TANK STORAGE MONITORING NODE     ")
print("=============================================\n")

print(f"Connecting to ModRSsim2 Simulator at {PLC_IP}:{PLC_PORT}...")
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
client.connect()
print("▶ Network Link Active.\n")

try:
    print("Polling register memory frame [Addresses 0-2]...")
    # Read 3 registers from address 0 using the verified device_id=1 parameter
    response = client.read_holding_registers(address=1, count=3, device_id=1)
    
    if not response.isError():
        raw_registers = response.registers
        print("✅ Telemetry package extracted successfully.")
        
        # Parse based on our industrial tank map configuration
        tank_level = raw_registers[0]          # Reg 0: 0-100%
        tank_temp = raw_registers[1] / 10.0    # Reg 1: Temp scaled by 10
        valve_status = "OPEN" if raw_registers[2] == 1 else "CLOSED" # Reg 2: Boolean status
        
        # Display Control Room Dashboard
        print("---------------------------------------------")
        print("          MAIN TANK FARM TELEMETRY           ")
        print("---------------------------------------------")
        print(f" Tank 1 Fill Level     : {tank_level}%")
        print(f" Tank 1 Internal Temp  : {tank_temp}°C")
        print(f" Main Discharge Valve  : {valve_status}")
        print("---------------------------------------------")
        
    else:
        print(f"❌ Protocol Read Aborted: {response}")

except Exception as e:
    print(f"💥 Critical Client Exception: {e}")

finally:
    client.close()
    print("\n▶ Connection closed cleanly. Telemetry node idling.")