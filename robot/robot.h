#ifndef ROBOT_H
#define ROBOT_H

#include "abdrive360.h"
#include "math.h"
#include "servo360.h"
#include "simpletools.h"
#include "servo.h"

#define PIN_SERVO_LEFT 12
#define PIN_SERVO_RIGHT 13
#define PIN_ENCODER_LEFT 14
#define PIN_ENCODER_RIGHT 15
#define PIN_SERVO_RELOAD 16

#define PIN_LED 9
#define PIN_LASER 10
#define PIN_FLYWHEELS 11

void init_robot();
void drive(int speed, int steering);
void drive_mm(int mm);
void init_robot();
void turn_on_place_relative(int angle);
void turn_on_place(int angle);
void drive_off();

void ask_for_dart();
void shoot();
void activate_laser(int turn_on);
void activate_shoot_motor(int turn_on);

#endif