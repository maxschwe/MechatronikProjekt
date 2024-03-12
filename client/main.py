from client import Client
from gui import Gui
import logging

HOST = "192.168.4.1"
PORT = 23

logging.basicConfig(level=logging.INFO)
logging.info("Connecting...")

client = Client(HOST, PORT)

gui = Gui(client)
gui.mainloop()
