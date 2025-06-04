import socket

# Server details
HOST = '127.0.0.1'
PORT = 7335

def main():
    # Create server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    try:
                        # Attempt to decode as UTF-8
                        keystrokes = data.decode('utf-8')
                    except UnicodeDecodeError:
                        # If decoding fails, log raw bytes as hex
                        keystrokes = f"Non-UTF8 data: {data.hex()}"
                    # Log keystrokes
                    with open('keylog.txt', 'a') as f:
                        f.write(keystrokes + '\n')
                    print(f"Received: {keystrokes}")

if __name__ == "__main__":
    main()