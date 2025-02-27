import socket


def start_client():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server running on localhost at port 8888
    client_socket.connect(('localhost', 8888))

    while True:
        # Get user input to send to the server
        message = input("You: ")

        n = 355
        e = 187

        # Convert each character to its ASCII code
        m = [ord(i) for i in message]

        # Encrypt each character using RSA encryption (using public key e, n)
        c = [(i ** e) % n for i in m]

        # Convert the list of encrypted numbers to a string and encode it to bytes
        client_socket.send(str(c).encode())

        # If the user enters "exit", break the loop and close connection
        if message.lower() == "exit":
            break

        # Receive and print the server's response (ciphertext)
        response = client_socket.recv(1024).decode()

        # Convert the response from string to a list of integers
        # It's important to safely evaluate the response into a list of integers
        c = eval(response)

        # Decrypt each number in the ciphertext using RSA decryption (private key d, n)
        n = 4717
        d = 3

        m = []
        for i in c:
            m.append(chr(pow(i, d, n)))  # Decrypt and convert back to character

        # Join the decrypted characters to form the original message
        decrypted_message = ''.join(m)

        # Print the decrypted message from the server
        print(f"Server: {decrypted_message}")

    # Close the client socket after exiting the loop
    client_socket.close()


# Run the client
start_client()
