def hex_to_dtc(hex_code: str) -> str:
    """
    Converts a hexadecimal internal code (4 or 6 digits) to a standard DTC (5 or 7 characters).
    Format: P/C/B/U + 4 digits (for 4-digit hex) or P/C/B/U + 4 digits + 2 hex chars (for 6-digit hex).
    Standard SAE J2012 decoding.
    """
    hex_code = hex_code.upper().strip()
    try:
        if len(hex_code) == 4:
            val = int(hex_code, 16)
            if val > 0xFFFF:
                return "Error: Code too large (max 4 hex digits)"
            
            byte0 = (val >> 8) & 0xFF
            byte1 = val & 0xFF
            
            system_map = {0: 'P', 1: 'C', 2: 'B', 3: 'U'}
            system_idx = (byte0 >> 6) & 0x03
            prefix = system_map[system_idx]
            
            type_digit = (byte0 >> 4) & 0x03
            digit3 = byte0 & 0x0F
            last_two = byte1
            
            return f"{prefix}{type_digit}{digit3:X}{last_two:02X}"
        elif len(hex_code) == 6:
            val_prefix = int(hex_code[:4], 16)
            if val_prefix > 0xFFFF:
                return "Error: Code prefix too large (max 4 hex digits)"
            
            byte0 = (val_prefix >> 8) & 0xFF
            byte1 = val_prefix & 0xFF
            
            system_map = {0: 'P', 1: 'C', 2: 'B', 3: 'U'}
            system_idx = (byte0 >> 6) & 0x03
            prefix = system_map[system_idx]
            
            type_digit = (byte0 >> 4) & 0x03
            digit3 = byte0 & 0x0F
            last_two_dtc = byte1
            
            # The last byte of the 3-byte hex code directly corresponds to the last two characters of the 7-char DTC
            last_byte_hex = hex_code[4:]
            
            return f"{prefix}{type_digit}{digit3:X}{last_two_dtc:02X}{last_byte_hex}"
        else:
            return "Error: Invalid Hex Code length (must be 4 or 6 digits)"
    except ValueError:
        return "Error: Invalid Hex Code"

def dtc_to_hex(dtc: str) -> str:
    """
    Converts a standard DTC (5 or 7 characters) to a hexadecimal internal code (4 or 6 digits).
    """
    dtc = dtc.upper().strip()
    
    try:
        if len(dtc) == 5:
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
            
            byte0 = (p_val << 6) | (digit2 << 4) | digit3
            byte1 = last_two
            
            val = (byte0 << 8) | byte1
            return f"{val:04X}"
        elif len(dtc) == 7:
            dtc_prefix = dtc[:5]
            last_two_chars = dtc[5:]

            prefix = dtc_prefix[0]
            prefix_map = {'P': 0, 'C': 1, 'B': 2, 'U': 3}
            if prefix not in prefix_map:
                return "Error: Invalid Prefix (must be P, C, B, U)"
            
            p_val = prefix_map[prefix]
            
            digit2 = int(dtc_prefix[1])
            if digit2 > 3:
                return "Error: 2nd digit must be 0-3"
                
            digit3 = int(dtc_prefix[2], 16)
            last_two_dtc = int(dtc_prefix[3:], 16)
            
            byte0 = (p_val << 6) | (digit2 << 4) | digit3
            byte1 = last_two_dtc
            
            val_prefix = (byte0 << 8) | byte1
            
            # The last two characters of the 7-char DTC directly correspond to the last byte of the 3-byte hex code
            last_byte_val = int(last_two_chars, 16)
            
            return f"{val_prefix:04X}{last_byte_val:02X}"
        else:
            return "Error: Invalid DTC format (must be 5 or 7 chars)"
    except ValueError:
        return "Error: Invalid characters in DTC"

if __name__ == "__main__":
    # Test cases for 4-digit hex / 5-char DTC
    print(f"0120 -> {hex_to_dtc('0120')}") # Expected P0120
    print(f"P0120 -> {dtc_to_hex('P0120')}") # Expected 0120
    
    print(f"4123 -> {hex_to_dtc('4123')}") # Expected C0123
    print(f"C0123 -> {dtc_to_hex('C0123')}") # Expected 4123
    
    print(f"D000 -> {hex_to_dtc('D000')}") # Expected U1000
    print(f"U1000 -> {dtc_to_hex('U1000')}") # Expected D000

    # Test cases for 6-digit hex / 7-char DTC
    print(f"0120FF -> {hex_to_dtc('0120FF')}") # Expected P0120FF
    print(f"P0120FF -> {dtc_to_hex('P0120FF')}") # Expected 0120FF

    print(f"4123AB -> {hex_to_dtc('4123AB')}") # Expected C0123AB
    print(f"C0123AB -> {dtc_to_hex('C0123AB')}") # Expected 4123AB

    print(f"D00012 -> {hex_to_dtc('D00012')}") # Expected U100012
    print(f"U100012 -> {dtc_to_hex('U100012')}") # Expected D00012

    print(f"Invalid Hex Length -> {hex_to_dtc('123')}") # Expected Error
    print(f"Invalid DTC Length -> {dtc_to_hex('P012')}") # Expected Error
    print(f"Invalid DTC Prefix -> {dtc_to_hex('X0120')}") # Expected Error
    print(f"Invalid DTC 2nd Digit -> {dtc_to_hex('P4120')}") # Expected Error
