import pymem
import time

def get_pointer_addr(pm, base, offsets):
    addr = pm.read_longlong(base)
    for offset in offsets[:-1]:
        addr = pm.read_longlong(addr + offset)
    return addr + offsets[-1]

def main():
    try:
        pm = pymem.Pymem("GeometryDash.exe")
    except pymem.exception.ProcessNotFound:
        print("Geometry Dash is not running.")
        return

    game_base = pm.base_address
    base_offset = 0x6C2ED8
    offsets = [0x208, 0x3084]

    print("Connected to geometry dash.")

    try:
        attempt_addr = get_pointer_addr(pm, game_base + base_offset, offsets)
        last_attempts = pm.read_int(attempt_addr)
        print(f"Monitoring started at Attempt: {last_attempts}")
        
    except pymem.exception.MemoryReadError:
        print("Please load into a level, and pause right away.")
        return

    while True:
        try:
            attempt_addr = get_pointer_addr(pm, game_base + base_offset, offsets)
            current_attempts = pm.read_int(attempt_addr)
            
            if current_attempts > last_attempts:

                if current_attempts == 10:

                    pm.write_int(attempt_addr, 67)
                    
                    current_attempts = 67

                print(f"DEATH DETECTED! (Attempt {current_attempts} now)")
                
                # TODO: ns time delay tracker here for backtracking. 
                # TODO: Create files for each type of mode + for backtracking.
                
                last_attempts = current_attempts
                time.sleep(0.5)

        except pymem.exception.MemoryReadError:
            pass

        time.sleep(0.001)

if __name__ == "__main__":
    main()