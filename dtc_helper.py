def hex_to_dtc(hex_code: str) -> str:
    """
    Converts a 4-digit hexadecimal internal code to a 5-character standard DTC.
    Format: P/C/B/U + 4 digits.
    Standard SAE J2012 decoding.
    """
    try:
        val = int(hex_code, 16)
        if val > 0xFFFF:
            return "Error: Code too large (max 4 hex digits)"
        
        byte0 = (val >> 8) & 0xFF
        byte1 = val & 0xFF
        
        # Bits 7-6 of High Byte: System
        system_map = {0: 'P', 1: 'C', 2: 'B', 3: 'U'}
        system_idx = (byte0 >> 6) & 0x03
        prefix = system_map[system_idx]
        
        # Bits 5-4 of High Byte: Code Type (0-3)
        type_digit = (byte0 >> 4) & 0x03
        
        # Bits 3-0 of High Byte: 3rd digit (Hex)
        digit3 = byte0 & 0x0F
        
        # Byte 1: Last 2 digits (Hex)
        last_two = byte1
        
        return f"{prefix}{type_digit}{digit3:X}{last_two:02X}"
    except ValueError:
        return "Error: Invalid Hex Code"

def dtc_to_hex(dtc: str) -> str:
    """
    Converts a 5-character standard DTC to a 4-digit hexadecimal internal code.
    """
    dtc = dtc.upper().strip()
    if len(dtc) != 5:
        return "Error: Invalid DTC format (must be 5 chars)"
    
    try:
        prefix = dtc[0]
        prefix_map = {'P': 0, 'C': 1, 'B': 2, 'U': 3}
        if prefix not in prefix_map:
            return "Error: Invalid Prefix (must be P, C, B, U)"
        
        p_val = prefix_map[prefix]
        
        digit2 = int(dtc[1])
        if digit2 > 3:
            return "Error: 2nd digit must be 0-3"
            
        digit3 = int(dtc[2], 16)
        last_two = int(dtc[3:], 16)
        
        # Reconstruct High Byte
        # Bits 7-6: p_val
        # Bits 5-4: digit2
        # Bits 3-0: digit3
        byte0 = (p_val << 6) | (digit2 << 4) | digit3
        
        # Reconstruct Low Byte
        byte1 = last_two
        
        val = (byte0 << 8) | byte1
        return f"{val:04X}"
    except ValueError:
        return "Error: Invalid characters in DTC"

if __name__ == "__main__":
    # Test cases
    print(f"0120 -> {hex_to_dtc('0120')}") # Expected P0120
    print(f"P0120 -> {dtc_to_hex('P0120')}") # Expected 0120
    
    print(f"4123 -> {hex_to_dtc('4123')}") # Expected C0123
    print(f"C0123 -> {dtc_to_hex('C0123')}") # Expected 4123
    
    print(f"D000 -> {hex_to_dtc('D000')}") # Expected U1000
    print(f"U1000 -> {dtc_to_hex('U1000')}") # Expected D000
