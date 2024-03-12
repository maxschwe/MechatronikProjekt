from tkinter import *
from customtkinter import *
import keyboard

from config import Config
from commands import Commands

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

    def btn_shoot_clicked(self):
        self.client.send_command(Commands.SHOOT)

    def key_clicked(self, event):
        if event.char == "a":
            self.speed.set(min(100, int(self.speed.get()) + Config.ACC_DEACC_AMOUNT))
        elif event.char == "d":
            self.speed.set(max(0, int(self.speed.get()) - Config.ACC_DEACC_AMOUNT))

    def handle_key_presses(self):
        up_pressed = keyboard.is_pressed("up")
        down_pressed = keyboard.is_pressed("down")
        left_pressed = keyboard.is_pressed("left")
        right_pressed = keyboard.is_pressed("right")
        try:
            configured_speed = int(self.speed.get())
        except:
            configured_speed = Config.DEFAULT_SPEED

        speed = 0
        steering = 0
        if up_pressed:
            speed = -configured_speed
            if left_pressed:
                steering = 50
            elif right_pressed:
                steering = -50
            else:
                steering = 0
        elif down_pressed:
            speed = configured_speed
            if left_pressed:
                steering = 50
            elif right_pressed:
                steering = -50
            else:
                steering = 0
        elif left_pressed:
            speed = configured_speed
            steering = -100
        elif right_pressed:
            speed = configured_speed
            steering = 100

        self.client.send_command(Commands.DRIVE, [speed, steering])

        self.after(Config.UPDATE_EVERY_IN_MS, self.handle_key_presses)