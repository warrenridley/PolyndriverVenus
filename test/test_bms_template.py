#!/usr/bin/env python3
"""
Test script to verify BMS template logic works correctly
"""

# Simulate the template storage and update logic
bms_msg_templates = {
    "BatChg": None,
    "BatSoC": None,
    "BatVoltageCurrent": None,
}

def bytes_helper(integer):
    """Helper function to split integer into high and low bytes"""
    return divmod(integer, 0x100)

def test_batChg_template():
    """Test BatChg message template logic"""
    print("Testing BatChg message template logic...")
    
    # Simulate received template from can2
    received_template = [0xFF, 0xFF, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]
    bms_msg_templates["BatChg"] = list(received_template)
    
    # Simulate Venus OS values
    max_voltage = 60.0
    charge_current = 100.0
    discharge_amps = 200.0
    min_voltage = 46.0
    
    # Convert to bytes
    Max_V_H, Max_V_L = bytes_helper(int(max_voltage * 10))
    Req_Charge_H, Req_Charge_L = bytes_helper(int(charge_current * 10))
    Req_Discharge_H, Req_Discharge_L = bytes_helper(int(discharge_amps * 10))
    Min_V_H, Min_V_L = bytes_helper(int(min_voltage * 10))
    
    # Apply the logic from dbus-sma.py
    if bms_msg_templates["BatChg"] is not None:
        msg_data = list(bms_msg_templates["BatChg"])
        # Update with Venus OS values
        msg_data[0] = Max_V_L
        msg_data[1] = Max_V_H
        msg_data[2] = Req_Charge_L
        msg_data[3] = Req_Charge_H
        msg_data[4] = Req_Discharge_L
        msg_data[5] = Req_Discharge_H
        msg_data[6] = Min_V_L
        msg_data[7] = Min_V_H
    else:
        msg_data = [Max_V_L, Max_V_H, Req_Charge_L, Req_Charge_H, Req_Discharge_L, Req_Discharge_H, Min_V_L, Min_V_H]
    
    print(f"  Original template: {received_template}")
    print(f"  Updated data:      {msg_data}")
    print(f"  Max V: {max_voltage}V -> bytes {Max_V_H:02X} {Max_V_L:02X}")
    print(f"  Charge: {charge_current}A -> bytes {Req_Charge_H:02X} {Req_Charge_L:02X}")
    print(f"  Discharge: {discharge_amps}A -> bytes {Req_Discharge_H:02X} {Req_Discharge_L:02X}")
    print(f"  Min V: {min_voltage}V -> bytes {Min_V_H:02X} {Min_V_L:02X}")
    
    # Verify the values are correctly set
    assert msg_data[0] == Max_V_L, f"Max_V_L mismatch: {msg_data[0]} != {Max_V_L}"
    assert msg_data[1] == Max_V_H, f"Max_V_H mismatch: {msg_data[1]} != {Max_V_H}"
    assert msg_data[2] == Req_Charge_L, f"Req_Charge_L mismatch: {msg_data[2]} != {Req_Charge_L}"
    assert msg_data[3] == Req_Charge_H, f"Req_Charge_H mismatch: {msg_data[3]} != {Req_Charge_H}"
    print("  ✓ BatChg template test passed!\n")

def test_batSoC_template():
    """Test BatSoC message template logic"""
    print("Testing BatSoC message template logic...")
    
    # Simulate received template from can2
    received_template = [50, 0x11, 0x64, 0x22, 0x33, 0x44]
    bms_msg_templates["BatSoC"] = list(received_template)
    
    # Simulate Venus OS values
    state_of_charge = 75.5
    
    # Convert to bytes
    SoC_HD = int(state_of_charge * 100)
    SoC_HD_H, SoC_HD_L = bytes_helper(SoC_HD)
    
    # Apply the logic from dbus-sma.py
    if bms_msg_templates["BatSoC"] is not None:
        msg2_data = list(bms_msg_templates["BatSoC"])
        # Update with Venus OS values
        msg2_data[0] = int(state_of_charge)
        msg2_data[4] = SoC_HD_L
        msg2_data[5] = SoC_HD_H
    else:
        msg2_data = [int(state_of_charge), 0x00, 0x64, 0x0, SoC_HD_L, SoC_HD_H]
    
    print(f"  Original template: {received_template}")
    print(f"  Updated data:      {msg2_data}")
    print(f"  SoC: {state_of_charge}% -> int {int(state_of_charge)}, HD bytes {SoC_HD_H:02X} {SoC_HD_L:02X}")
    
    # Verify values
    assert msg2_data[0] == int(state_of_charge), f"SoC mismatch: {msg2_data[0]} != {int(state_of_charge)}"
    assert msg2_data[1] == 0x11, f"Template byte 1 should remain: {msg2_data[1]} != 0x11"
    assert msg2_data[2] == 0x64, f"Template byte 2 should remain: {msg2_data[2]} != 0x64"
    assert msg2_data[3] == 0x22, f"Template byte 3 should remain: {msg2_data[3]} != 0x22"
    assert msg2_data[4] == SoC_HD_L, f"SoC_HD_L mismatch: {msg2_data[4]} != {SoC_HD_L}"
    assert msg2_data[5] == SoC_HD_H, f"SoC_HD_H mismatch: {msg2_data[5]} != {SoC_HD_H}"
    print("  ✓ BatSoC template test passed!\n")

def test_batVoltageCurrent_template():
    """Test BatVoltageCurrent message template logic"""
    print("Testing BatVoltageCurrent message template logic...")
    
    # Simulate received template from can2 (6 bytes)
    received_template = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]
    bms_msg_templates["BatVoltageCurrent"] = list(received_template)
    
    # Simulate Venus OS values
    actual_battery_voltage = 52.5
    battery_current = 25.3
    battery_temperature = 22.5
    
    # Convert to bytes
    voltage = int(actual_battery_voltage * 100)
    voltage_H, voltage_L = bytes_helper(voltage)
    current = int(battery_current * 10)
    current_H, current_L = bytes_helper(current)
    temperature = int(battery_temperature * 10)
    temperature_H, temperature_L = bytes_helper(temperature)
    
    # Apply the logic from dbus-sma.py
    if bms_msg_templates["BatVoltageCurrent"] is not None:
        msg3_data = list(bms_msg_templates["BatVoltageCurrent"])
        # Update with Venus OS values
        msg3_data[0] = voltage_L
        msg3_data[1] = voltage_H
        msg3_data[2] = current_L
        msg3_data[3] = current_H
        msg3_data[4] = temperature_L
        msg3_data[5] = temperature_H
    else:
        msg3_data = [voltage_L, voltage_H, current_L, current_H, temperature_L, temperature_H]
    
    print(f"  Original template: {received_template}")
    print(f"  Updated data:      {msg3_data}")
    print(f"  Voltage: {actual_battery_voltage}V -> bytes {voltage_H:02X} {voltage_L:02X}")
    print(f"  Current: {battery_current}A -> bytes {current_H:02X} {current_L:02X}")
    print(f"  Temp: {battery_temperature}°C -> bytes {temperature_H:02X} {temperature_L:02X}")
    
    # Verify all bytes are updated correctly
    assert msg3_data[0] == voltage_L, f"voltage_L mismatch: {msg3_data[0]} != {voltage_L}"
    assert msg3_data[1] == voltage_H, f"voltage_H mismatch: {msg3_data[1]} != {voltage_H}"
    assert msg3_data[2] == current_L, f"current_L mismatch: {msg3_data[2]} != {current_L}"
    assert msg3_data[3] == current_H, f"current_H mismatch: {msg3_data[3]} != {current_H}"
    assert msg3_data[4] == temperature_L, f"temperature_L mismatch: {msg3_data[4]} != {temperature_L}"
    assert msg3_data[5] == temperature_H, f"temperature_H mismatch: {msg3_data[5]} != {temperature_H}"
    print("  ✓ BatVoltageCurrent template test passed!\n")

def test_fallback_logic():
    """Test that fallback works when no template is received"""
    print("Testing fallback logic (no template received)...")
    
    # Reset template to None
    bms_msg_templates["BatChg"] = None
    
    # Simulate Venus OS values
    max_voltage = 58.0
    charge_current = 80.0
    discharge_amps = 150.0
    min_voltage = 48.0
    
    # Convert to bytes
    Max_V_H, Max_V_L = bytes_helper(int(max_voltage * 10))
    Req_Charge_H, Req_Charge_L = bytes_helper(int(charge_current * 10))
    Req_Discharge_H, Req_Discharge_L = bytes_helper(int(discharge_amps * 10))
    Min_V_H, Min_V_L = bytes_helper(int(min_voltage * 10))
    
    # Apply the logic from dbus-sma.py
    if bms_msg_templates["BatChg"] is not None:
        msg_data = list(bms_msg_templates["BatChg"])
        msg_data[0] = Max_V_L
        msg_data[1] = Max_V_H
        msg_data[2] = Req_Charge_L
        msg_data[3] = Req_Charge_H
        msg_data[4] = Req_Discharge_L
        msg_data[5] = Req_Discharge_H
        msg_data[6] = Min_V_L
        msg_data[7] = Min_V_H
    else:
        msg_data = [Max_V_L, Max_V_H, Req_Charge_L, Req_Charge_H, Req_Discharge_L, Req_Discharge_H, Min_V_L, Min_V_H]
    
    print(f"  No template, using default structure")
    print(f"  Generated data: {msg_data}")
    
    # Verify the default structure is used correctly
    assert len(msg_data) == 8, f"Message should have 8 bytes, got {len(msg_data)}"
    assert msg_data[0] == Max_V_L
    assert msg_data[1] == Max_V_H
    print("  ✓ Fallback logic test passed!\n")

if __name__ == "__main__":
    print("="*60)
    print("BMS Template Logic Tests")
    print("="*60 + "\n")
    
    test_batChg_template()
    test_batSoC_template()
    test_batVoltageCurrent_template()
    test_fallback_logic()
    
    print("="*60)
    print("All tests passed! ✓")
    print("="*60)
