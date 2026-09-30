import os
import time
import signal
import subprocess
import sys
import random

# --- COLOR PALETTE & STYLING ---
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BG_DARK = '\033[40m'

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def error(message):
    print(f"\n{Color.RED}{Color.BOLD}[!] ERROR:{Color.RESET} {Color.RED}{message}{Color.RESET}")

def dashboard_banner(status_mode="IDLE"):
    mode_color = Color.GREEN if status_mode == "RECORDING" else (Color.RED if status_mode == "ATTACK" else Color.CYAN)
    print(f"""{Color.CYAN}
▐▓▓▓▓▓▌▐▓▓▓▓▌▐▓▌▐▓▌▐▓▓▓▓▌▐▓▓▓▓▌▐▓▌ ▐▓▌▐▓▓▓▓▌ ▐▓▌▐▓▌▐▓▓▓▓▌
  ▐▓▌  ▐▓▌▐▓▌▐▓▌▐▓▌▐▓▌   ▐▓▌▐▓▌▐▓▓▌▐▓▌▐▓▌ ▐▓▌▐▓▌▐▓▌▐▓▌   
  ▐▓▌  ▐▓▌▐▓▌▐▓▌▐▓▌▐▓▌   ▐▓▓▓▓▌▐▓▐▓▐▓▌▐▓▓▓▓▓▌▐▓▌▐▓▌▐▓▓▓▓▌
  ▐▓▌  ▐▓▌▐▓▌▐▓▌▐▓▌▐▓▌   ▐▓▌▐▓▌▐▓▌▐▓▓▌▐▓▌ ▐▓▌▐▓▌▐▓▌   ▐▓▌
  ▐▓▌  ▐▓▓▓▓▌▐▓▓▓▓▌▐▓▓▓▓▌▐▓▌▐▓▌▐▓▌ ▐▓▌▐▓▓▓▓▌ ▐▓▓▓▓▌▐▓▓▓▓▌
                     AUTOMATION SUITE v3.1 [{mode_color}{status_mode}{Color.CYAN}]{Color.RESET}
""")

def status_panel(canFile, bitRate, pluggedIn, activeFilter, activeDbc):
    device_status = f"{Color.GREEN}{Color.BOLD}● ONLINE{Color.RESET}" if pluggedIn == 1 else f"{Color.RED}{Color.BOLD}● OFFLINE{Color.RESET}"
    
    print(f"{Color.DIM}┌───────────────────────────── SYSTEM STATUS ──────────────────────────────┐{Color.RESET}")
    print(f"│  {Color.BOLD}Bitrate:{Color.RESET} {Color.YELLOW}{bitRate:<12}{Color.RESET}  │  {Color.BOLD}CAN Device:{Color.RESET} {device_status:<17}  │")
    print(f"│  {Color.BOLD}Log File:{Color.RESET} {Color.CYAN}{str(canFile)[:15]:<13}{Color.RESET}  │  {Color.BOLD}Filter Profile:{Color.RESET} {Color.MAGENTA}{str(activeFilter)[:12]:<13}{Color.RESET}  │")
    print(f"│  {Color.BOLD}DBC Profile:{Color.RESET} {Color.BLUE}{str(activeDbc)[:13]:<12}{Color.RESET}  │                                           │")
    print(f"{Color.DIM}└──────────────────────────────────────────────────────────────────────────┘{Color.RESET}")

def help_menu():
    clear_screen()
    dashboard_banner("HELP")
    print(f"{Color.BOLD}=== TOUCANBus Comprehensive Guide ==={Color.RESET}")
    print(f" {Color.CYAN}[1]{Color.RESET} Record Traffic : Captures live SocketCAN frames into a log file.")
    print(f" {Color.CYAN}[2]{Color.RESET} Dump CAN       : Real-time packet analysis using cansniffer.")
    print(f" {Color.CYAN}[3]{Color.RESET} Log Manager    : Switch between recorded session files.")
    print(f" {Color.CYAN}[4]{Color.RESET} Parser/Decoder : Search IDs, strip traffic, or decode with DBC.")
    print(f" {Color.CYAN}[5]{Color.RESET} Replay Log     : Transmit recorded logs back onto the bus via canplayer.")
    print(f" {Color.CYAN}[6]{Color.RESET} Fuzzer Suite   : Automated payload and UDS service brute-forcing.")
    print(f" {Color.CYAN}[7]{Color.RESET} Custom Frame   : Send a single manual CAN payload.")
    print(f" {Color.CYAN}[8]{Color.RESET} Filters        : Apply custom SocketCAN masking rules.")
    print(f" {Color.CYAN}[9]{Color.RESET} DBC Profiles   : Load signal definitions for human translation.")
    input(f"\n{Color.YELLOW}[PRESS ENTER TO RETURN TO DASHBOARD]{Color.RESET}")

def check_can_device():
    try:
        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        return 1 if "can0" in result.stdout else 0
    except Exception:
        return 0

def play_code(canFile, bitRate, pluggedIn, activeFilter, activeDbc):
    clear_screen()
    dashboard_banner("ATTACK")
    status_panel(canFile, bitRate, pluggedIn, activeFilter, activeDbc)
    indCode = input(f"\n{Color.BOLD} Enter CAN Code (e.g., 123#00010203): {Color.RESET}")
    print(f"\n{Color.YELLOW}[*] Transmitting custom payload...", end="")
    
    for _ in range(4):
        time.sleep(0.2)
        print(".", end="", flush=True)
    
    try:
        subprocess.run(["cansend", "can0", indCode], check=True)
        print(f" {Color.GREEN}{Color.BOLD}[SUCCESS]{Color.RESET}")
    except subprocess.CalledProcessError:
        error("Transmission failed. Verify interface state.")
    time.sleep(1.2)

def parse_dbc(dbc_path):
    messages = {}
    if not os.path.exists(dbc_path):
        return messages
    try:
        with open(dbc_path, 'r') as f:
            for line in f:
                if line.startswith("BO_ "):
                    parts = line.strip().split()
                    can_id_dec = int(parts[1])
                    msg_name = parts[2].rstrip(":")
                    messages[f"{can_id_dec:X}"] = msg_name
    except Exception:
        pass
    return messages

def file_parse(canFile, bitRate, pluggedIn, activeFilter, activeDbc):
    clear_screen()
    dashboard_banner("PARSER")
    status_panel(canFile, bitRate, pluggedIn, activeFilter, activeDbc)
    
    log_path = os.path.join("logs", canFile)
    if not os.path.exists(log_path):
        error("Selected log file not found.")
        time.sleep(1.5)
        return

    print(f"\n {Color.BOLD}LOG PARSING OPERATIONS:{Color.RESET}")
    print(f"   {Color.GREEN}[1]{Color.RESET} Search/Filter CAN ID")
    print(f"   {Color.GREEN}[2]{Color.RESET} Strip/Remove CAN ID from Log")
    print(f"   {Color.GREEN}[3]{Color.RESET} Decode with Active DBC Profile")
    print(f"   {Color.RED}[Q]{Color.RESET} Return to Dashboard")
    
    choice = input(f"\n{Color.YELLOW}Select Action > {Color.RESET}").strip().upper()
    if choice == "1":
        search_id = input("Enter CAN ID to search (e.g., 123): ").strip()
        print(f"\n{Color.CYAN}--- Search Results for ID: {search_id} ---{Color.RESET}")
        with open(log_path, 'r') as f:
            lines = [line for line in f if search_id.lower() in line.lower()]
            for line in lines[:20]:
                print(line.strip())
            print(f"\nTotal matching frames: {len(lines)}")
        input(f"\n{Color.YELLOW}[PRESS ENTER TO CONTINUE]{Color.RESET}")
    elif choice == "2":
        remove_id = input("Enter CAN ID to strip: ").strip()
        temp_file = "logs/temp.log"
        with open(log_path, 'r') as infile, open(temp_file, 'w') as outfile:
            for line in infile:
                if remove_id.lower() not in line.lower():
                    outfile.write(line)
        os.replace(temp_file, log_path)
        print(f"{Color.GREEN}[+] Log file successfully filtered and updated!{Color.RESET}")
        time.sleep(1.5)
    elif choice == "3":
        dbc_map = parse_dbc(os.path.join("dbc", activeDbc)) if activeDbc != "NONE" else {}
        print(f"\n{Color.CYAN}--- DBC Signal Translation ---{Color.RESET}")
        with open(log_path, 'r') as f:
            count = 0
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    can_id = parts[2]
                    decoded_name = dbc_map.get(can_id, "UNKNOWN_SIGNAL")
                    print(f" ID: {can_id:<6} │ Signal: {decoded_name:<18} │ Raw: {line.strip()}")
                    count += 1
                    if count >= 25:
                        print(f"{Color.DIM}... (Truncated to first 25 entries){Color.RESET}")
                        break
        input(f"\n{Color.YELLOW}[PRESS ENTER TO CONTINUE]{Color.RESET}")

def can_files(canFile, bitRate, pluggedIn, activeFilter, activeDbc):
    clear_screen()
    dashboard_banner("LOG SELECTOR")
    status_panel(canFile, bitRate, pluggedIn, activeFilter, activeDbc)
    
    if not os.path.exists("logs"):
        os.makedirs("logs")
        
    files = [f for f in os.listdir("logs") if f.endswith(".log")]
    if not files:
        print(f"\n{Color.YELLOW}[!] No log files available in 'logs/' directory.{Color.RESET}")
        input(f"\n{Color.YELLOW}[PRESS ENTER TO CONTINUE]{Color.RESET}")
        return canFile

    print(f"\n {Color.BOLD}AVAILABLE LOG FILES:{Color.RESET}")
    log_files = {i: f for i, f in enumerate(files)}
    for k, v in log_files.items():
        print(f"   {Color.CYAN}[{k}]{Color.RESET} {v}")
    print(f"   {Color.RED}[B]{Color.RESET} Back")
    
    selection = input(f"\n{Color.YELLOW}Select Log Index > {Color.RESET}").strip().upper()
    if selection == "B":
        return canFile
    try:
        return log_files[int(selection)]
    except (ValueError, KeyError):
        error("Invalid index selection.")
        time.sleep(1)
        return canFile

def record_can(canFile, bitRate, pluggedIn, filterConfig, activeDbc):
    clear_screen()
    dashboard_banner("RECORDING")
    status_panel(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
    
    file_name = input(f"\n{Color.YELLOW}Enter Session Filename (no extension) > {Color.RESET}").strip()
    if not file_name:
        file_name = "capture"
    file_name += ".log"
    
    print(f"\n{Color.RED}{Color.BOLD}[!] RECORDER LIVE: Press 'Q' then ENTER to terminate session.{Color.RESET}\n")
    
    cmd = ["candump", "-l", "can0"]
    if filterConfig != "NONE":
        cmd = ["candump", "-l", f"can0,{filterConfig}"]
        
    recorder = subprocess.Popen(cmd)
    
    try:
        while True:
            if input().strip().lower() == 'q':
                break
    except KeyboardInterrupt:
        pass
    
    recorder.terminate()
    recorder.wait()
    
    os.system(f"find . -type f -name 'candump*' -exec cp {{}} logs/{file_name} \;")
    os.system("find . -type f -name 'candump*' -delete")
    print(f"{Color.GREEN}[+] Capture saved successfully as '{file_name}'!{Color.RESET}")
    time.sleep(1.5)

def find_code(canFile, bitRate, pluggedIn, activeFilter, activeDbc):
    clear_screen()
    dashboard_banner("FUZZER SUITE")
    status_panel(canFile, bitRate, pluggedIn, activeFilter, activeDbc)
    print(f"\n{Color.YELLOW}{Color.BOLD}[!] WARNING: Fuzzing triggers rapid state changes on vehicle buses.{Color.RESET}")
    
    print(f"\n {Color.BOLD}SELECT ATTACK VECTOR:{Color.RESET}")
    print(f"   {Color.MAGENTA}[1]{Color.RESET} Incremental Byte Fuzzer")
    print(f"   {Color.MAGENTA}[2]{Color.RESET} Random Entropy Payload Fuzzer")
    print(f"   {Color.MAGENTA}[3]{Color.RESET} UDS Service ID Brute-forcer")
    print(f"   {Color.RED}[B]{Color.RESET} Back")
    
    mode = input(f"\n{Color.YELLOW}Select Mode > {Color.RESET}").strip().upper()
    if mode == "B":
        return

    target_id = input("Enter Target CAN ID (e.g., 7E0): ").strip()
    if not target_id:
        return
        
    confirm = input(f"Confirm execution on ID [{target_id}]? (y/N): ").strip().lower()
    if confirm != 'y':
        return
        
    print(f"\n{Color.RED}[*] Attack payload stream initialized... Press Ctrl+C to abort.{Color.RESET}")
    try:
        if mode == "1":
            for byte1 in range(0, 256):
                payload = f"{target_id}#01{byte1:02X}000000000000"
                subprocess.run(["cansend", "can0", payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                sys.stdout.write(f"\r[SENDING] {payload}")
                sys.stdout.flush()
                time.sleep(0.005)
        elif mode == "2":
            while True:
                rand_bytes = "".join([f"{random.randint(0, 255):02X}" for _ in range(8)])
                payload = f"{target_id}#{rand_bytes}"
                subprocess.run(["cansend", "can0", payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                sys.stdout.write(f"\r[SENDING] {payload}")
                sys.stdout.flush()
                time.sleep(0.01)
        elif mode == "3":
            for sid in range(0x10, 0x40):
                payload = f"{target_id}#02{sid:02X}000000000000"
                subprocess.run(["cansend", "can0", payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                sys.stdout.write(f"\r[TESTING UDS] SID: {sid:02X}")
                sys.stdout.flush()
                time.sleep(0.05)
    except KeyboardInterrupt:
        print(f"\n{Color.GREEN}[+] Fuzzing halted safely by operator.{Color.RESET}")
    input(f"\n{Color.YELLOW}[PRESS ENTER TO CONTINUE]{Color.RESET}")

def manage_filters(canFile, bitRate, pluggedIn, activeFilter, activeDbc):
    clear_screen()
    dashboard_banner("FILTERS")
    status_panel(canFile, bitRate, pluggedIn, activeFilter, activeDbc)
    
    print(f"\n {Color.BOLD}SOCKETCAN FILTER CONFIGURATION:{Color.RESET}")
    print(f"   {Color.CYAN}[1]{Color.RESET} Set Custom Filter Pattern (e.g., 128:7FF)")
    print(f"   {Color.CYAN}[2]{Color.RESET} Clear / Reset Filter Rules")
    print(f"   {Color.RED}[B]{Color.RESET} Back")
    
    choice = input(f"\n{Color.YELLOW}Select Option > {Color.RESET}").strip().upper()
    if choice == "1":
        f_str = input("Enter rule pattern (<canID>:<mask>) > ").strip()
        if f_str:
            return f_str
    elif choice == "2":
        return "NONE"
    return activeFilter

def manage_dbc(activeDbc):
    clear_screen()
    dashboard_banner("DBC PROFILES")
    
    if not os.path.exists("dbc"):
        os.makedirs("dbc")
        
    files = [f for f in os.listdir("dbc") if f.endswith(".dbc")]
    if not files:
        print(f"\n{Color.YELLOW}[!] No DBC database files found in 'dbc/' directory.{Color.RESET}")
        print("Drop standard .dbc files into the 'dbc/' folder to load profiles.")
        input(f"\n{Color.YELLOW}[PRESS ENTER TO CONTINUE]{Color.RESET}")
        return activeDbc

    print(f"\n {Color.BOLD}LOADED DBC PROFILES:{Color.RESET}")
    dbc_files = {i: f for i, f in enumerate(files)}
    for k, v in dbc_files.items():
        print(f"   {Color.BLUE}[{k}]{Color.RESET} {v}")
    print(f"   {Color.RED}[B]{Color.RESET} Back")
    
    selection = input(f"\n{Color.YELLOW}Select Profile Index > {Color.RESET}").strip().upper()
    if selection == "B":
        return activeDbc
    try:
        return dbc_files[int(selection)]
    except (ValueError, KeyError):
        error("Invalid index.")
        time.sleep(1)
        return activeDbc

def main():
    if os.geteuid() != 0:
        print(f"{Color.YELLOW}[!] Notice: Running without root/sudo privileges may restrict CAN operations.{Color.RESET}")

    for d in ["logs", "filters", "checks", "dbc"]:
        if not os.path.exists(d):
            os.makedirs(d)

    clear_screen()
    dashboard_banner("INIT")
    bitRate = input(f"{Color.YELLOW}Enter desired bus bitrate [Default: 500000] > {Color.RESET}").strip()
    if not bitRate:
        bitRate = "500000"
        
    os.system(f"sudo ip link set can0 up type can bitrate {bitRate} 2>/dev/null")
    os.system("sudo ifconfig can0 txqueuelen 1000 2>/dev/null")
    
    canFile = f"{Color.RED}NONE{Color.RESET}"
    filterConfig = "NONE"
    activeDbc = "NONE"

    while True:
        pluggedIn = check_can_device()
        clear_screen()
        dashboard_banner("IDLE")
        status_panel(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
        
        # Gorgeous Dual-Column Dashboard Grid
        print(f"\n{Color.DIM}┌────────────────────────────── DASHBOARD MENU ────────────────────────────┐{Color.RESET}")
        print(f"│  {Color.GREEN}[1]{Color.RESET} Record CAN Traffic       │  {Color.CYAN}[6]{Color.RESET} Automated Fuzzer Suite       │")
        print(f"│  {Color.GREEN}[2]{Color.RESET} Dump CAN (cansniffer)    │  {Color.CYAN}[7]{Color.RESET} Play Specific CAN Code       │")
        print(f"│  {Color.GREEN}[3]{Color.RESET} Select CAN Logs          │  {Color.MAGENTA}[8]{Color.RESET} Configure Bus Filters        │")
        print(f"│  {Color.GREEN}[4]{Color.RESET} Parse & Decode Log       │  {Color.MAGENTA}[9]{Color.RESET} Load DBC Profile             │")
        print(f"│  {Color.GREEN}[5]{Color.RESET} Replay Log File          │  {Color.BLUE}[H]{Color.RESET} Help Documentation           │")
        print(f"│                             │  {Color.YELLOW}[R]{Color.RESET} Refresh Dashboard            │")
        print(f"│                             │  {Color.RED}[B]{Color.RESET} Exit Suite                   │")
        print(f"{Color.DIM}└──────────────────────────────────────────────────────────────────────────┘{Color.RESET}")
        
        choice = input(f"{Color.YELLOW} TOUCANBus > {Color.RESET}").strip().upper()
        
        if choice == "1":
            if pluggedIn: record_can(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
            else: error("CAN interface 'can0' is offline!"); time.sleep(1.5)
        elif choice == "2":
            if pluggedIn: os.system("cansniffer -c can0")
            else: error("CAN interface 'can0' is offline!"); time.sleep(1.5)
        elif choice == "3":
            canFile = can_files(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
        elif choice == "4":
            if "NONE" in canFile: error("Please select a valid log file first!"); time.sleep(1.5)
            else: file_parse(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
        elif choice == "5":
            if "NONE" in canFile: error("Please select a valid log file first!"); time.sleep(1.5)
            else:
                clear_screen()
                dashboard_banner("ATTACK")
                status_panel(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
                print(f"\n{Color.YELLOW}[*] Replaying log session onto can0...{Color.RESET}")
                time.sleep(1)
                os.system(f"cd logs && canplayer -I {canFile}")
                input(f"\n{Color.YELLOW}[PRESS ENTER TO CONTINUE]{Color.RESET}")
        elif choice == "6":
            if pluggedIn: find_code(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
            else: error("CAN interface 'can0' is offline!"); time.sleep(1.5)
        elif choice == "7":
            if pluggedIn: play_code(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
            else: error("CAN interface 'can0' is offline!"); time.sleep(1.5)
        elif choice == "8":
            filterConfig = manage_filters(canFile, bitRate, pluggedIn, filterConfig, activeDbc)
        elif choice == "9":
            activeDbc = manage_dbc(activeDbc)
        elif choice == "H":
            help_menu()
        elif choice == "R":
            continue
        elif choice == "B":
            print(f"\n{Color.CYAN}Shutting down TOUCANBus. Drive safely!{Color.RESET}\n")
            break
        else:
            error("Invalid choice selected.")
            time.sleep(1.2)

if __name__ == "__main__":
    main()
