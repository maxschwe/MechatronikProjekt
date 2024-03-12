import logging
import socket

class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        self.connected = False
        try:
            self.socket.connect((host, port))
            logging.info("Connected to robot successfully")
            self.connected = True
        except socket.timeout:
            logging.warning("Failed to connect to robot")
        
    def send_command(self, cmd, params = None):
        cmd_string = str(cmd)
        if params is not None:
            cmd_string += ";" + ";".join(map(str, params))
        if not self.connected:
            logging.warning(f"Failed to send '{cmd_string}' because bot is not connected")
            return
        logging.info(f'Sending "{cmd_string}"')
        cmd_string += "\n"
        self.socket.send(cmd_string.encode())
