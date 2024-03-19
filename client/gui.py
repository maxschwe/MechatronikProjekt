from tkinter import *
from customtkinter import *
import keyboard

from config import Config
from commands import Commands

from pydualsense import *
# create dualsense
dualsense = pydualsense()
# find device and initialize
dualsense.init()

set_appearance_mode("dark")
set_default_color_theme("blue")


class Gui(CTk):
    def __init__(self, client):
        CTk.__init__(self)
        self.client = client
        self.title("Roboter Controller")
        self.geometry("300x400+700+300")

        self.is_laser_on = False
        self.is_shoot_motor_on = False

        self.setup_ui()
        self.bind("<KeyRelease>", self.key_clicked)
        self.handle_key_presses()

    def setup_ui(self):
        self.main_frame = CTkFrame(self)
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.lbl_speed = CTkLabel(self.main_frame, text="Geschwindigkeit")
        self.lbl_speed.pack()

        self.speed = StringVar(value=Config.DEFAULT_SPEED)
        self.sb_speed = CTkEntry(self.main_frame, textvariable=self.speed)
        self.sb_speed.pack(pady=10)

        self.btn_ask_for_dart = CTkButton(self.main_frame, text="Dart anfordern", command=self.btn_ask_for_dart_clicked)
        self.btn_ask_for_dart.pack(fill=BOTH, expand=1, pady=10)

        self.btn_laser = CTkButton(self.main_frame, text="Laser an", command=self.btn_laser_clicked)
        self.btn_laser.pack(fill=BOTH, expand=1, pady=10)

        self.btn_shoot_motor = CTkButton(self.main_frame, text="Motoren an", command=self.btn_shoot_motor_clicked)
        self.btn_shoot_motor.pack(fill=BOTH, expand=1, pady=10)

        self.btn_shoot = CTkButton(self.main_frame, text="Schießen", command=self.btn_shoot_clicked)
        self.btn_shoot.pack(fill=BOTH, expand=1, pady=10)

        self.btn_move_servo = CTkButton(self.main_frame, text="Nachschieben", command=self.btn_move_servo_clicked)
        self.btn_move_servo.pack(fill=BOTH, expand=1, pady=10)

    def btn_ask_for_dart_clicked(self):
        self.client.send_command(Commands.ASK_FOR_DART)

    def btn_laser_clicked(self):
        self.is_laser_on = not self.is_laser_on
        if self.is_laser_on:
            self.btn_laser.configure(text="Laser aus")
        else:
            self.btn_laser.configure(text="Laser an")
        self.client.send_command(Commands.LASER, [int(self.is_laser_on)])

    def btn_shoot_motor_clicked(self):
        self.is_shoot_motor_on = not self.is_shoot_motor_on
        if self.is_shoot_motor_on:
            self.btn_shoot_motor.configure(text="Motoren aus")
        else:
            self.btn_shoot_motor.configure(text="Motoren an")
        self.client.send_command(Commands.SHOOT_MOTOR_ON, [int(self.is_shoot_motor_on)])

    def btn_move_servo_clicked(self):
        self.client.send_command(Commands.MOVE_SERVO)

    def btn_shoot_clicked(self):
        self.client.send_command(Commands.SHOOT)

    def key_clicked(self, event):
        if event.char == "a":
            self.speed.set(min(100, int(self.speed.get()) + Config.ACC_DEACC_AMOUNT))
        elif event.char == "d":
            self.speed.set(max(0, int(self.speed.get()) - Config.ACC_DEACC_AMOUNT))

    def handle_key_presses(self):
        self.is_laser_on = not self.is_laser_on
        self.is_shoot_motor_on = not self.is_shoot_motor_on
        speed = 0
        
        if dualsense.state.R2 > 0.1:
            speed = -1 * dualsense.state.R2
        else:
            speed = dualsense.state.L2     
        if dualsense.state.circle:
            self.client.send_command(Commands.SHOOT)
        if dualsense.state.triangle:
            self.client.send_command(Commands.MOVE_SERVO)
        if dualsense.state.square:
            self.client.send_command(Commands.SHOOT_MOTOR_ON, [int(self.is_shoot_motor_on)])
        if dualsense.state.DpadDown:
            self.client.send_command(Commands.ASK_FOR_DART)
        if dualsense.state.DpadUp:
            self.client.send_command(Commands.LASER, [int(self.is_laser_on)])
            
        self.client.send_command(Commands.DRIVE, [speed, dualsense.state.LX])
        self.after(Config.UPDATE_EVERY_IN_MS, self.handle_key_presses_dualsense)
