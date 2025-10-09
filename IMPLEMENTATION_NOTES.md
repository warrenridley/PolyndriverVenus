# BMS CAN Message Template Implementation

## Overview
This implementation modifies `dbus-sma.py` to receive BMS CAN messages from `can2`, learn their format, and then transmit BMS messages to `can5` using Venus OS values in the same format as received.

## Changes Made

### 1. Added Second CAN Bus (`can2`)
- **Variable**: `canBusChannelBMS = "can2"`
- **Purpose**: Dedicated channel for receiving BMS messages
- **Initialization**: Added in `__init__()` with error handling for when the bus is not available

### 2. BMS Message Template Storage
```python
bms_msg_templates = {
  "BatChg": None,          # 0x351
  "BatSoC": None,          # 0x355
  "BatVoltageCurrent": None,  # 0x356
  "BatStatus": None,       # 0x359
  "AlarmWarning": None,    # 0x35a
  "BMSOem": None,          # 0x35e
  "BatData": None          # 0x35f
}
```

### 3. New Handler: `_parse_bms_can_data_handler()`
- Called every 20ms (same frequency as main CAN handler)
- Reads all available messages from `can2` (non-blocking)
- Stores message data as templates for each BMS message type
- Only stores messages with matching arbitration IDs

### 4. Updated Transmit Handler: `_can_bus_txmit_handler()`
Each message now uses this pattern:
```python
if bms_msg_templates["MessageType"] is not None:
    msg_data = list(bms_msg_templates["MessageType"])
    # Update specific bytes with Venus OS values
    msg_data[byte_index] = venus_os_value
else:
    # Fallback to default hardcoded values
    msg_data = [default, values, ...]
```

### 5. Message-Specific Updates

#### BatChg (0x351) - Battery Charge Parameters
Updates bytes 0-7 with:
- Max voltage (bytes 0-1)
- Requested charge current (bytes 2-3)
- Requested discharge current (bytes 4-5)
- Min voltage (bytes 6-7)

#### BatSoC (0x355) - State of Charge
Updates bytes 0, 4-5 with:
- SOC integer percentage (byte 0)
- SOC high definition (bytes 4-5)

#### BatVoltageCurrent (0x356) - Battery Voltage/Current/Temperature
Updates all 6 bytes with:
- Voltage (bytes 0-1)
- Current (bytes 2-3)
- Temperature (bytes 4-5)

#### Other Messages
- AlarmWarning (0x35a): Uses template as-is or defaults to zeros
- BMSOem (0x35e): Uses template as-is or defaults to "BATRIUM "
- BatData (0x35f): Uses template as-is or defaults to battery data structure
- BatStatus (0x359): Uses template as-is or defaults to status bytes

## Data Flow

```
can2 (BMS) → _parse_bms_can_data_handler() → bms_msg_templates (stored)
                                                      ↓
Venus OS D-Bus → _can_bus_txmit_handler() → Apply values to templates → can5 (SMA)
```

## Backward Compatibility
- If `can2` is not connected: Error logged, templates remain `None`, defaults used
- If BMS messages not received: Templates remain `None`, defaults used
- Existing SMA data reception from `can5` unchanged
- BMS charge controller logic unchanged

## Testing
Created `test/test_bms_template.py` to verify:
- Template storage and value update logic
- Correct byte manipulation for all message types
- Fallback to defaults when templates unavailable
- All tests pass ✓

## Benefits
1. **Format Compatibility**: Messages sent to SMA match the exact format from the actual BMS
2. **Flexibility**: Supports different BMS manufacturers without code changes
3. **Robustness**: Graceful fallback when can2 is not available
4. **Maintainability**: Clear separation of template learning and value injection
