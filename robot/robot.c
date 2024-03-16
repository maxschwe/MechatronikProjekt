#include "robot.h"

volatile int shoot_motor_is_on;


void drive(int speed, int steering)
{
    int speed_left, speed_right;
    if (steering > 0)
    {
        speed_left = speed;
        speed_right = speed * (1 - steering / 50.0);
    }
    else
    {
        speed_left = speed * (1 + steering / 50.0);
        speed_right = speed;
    }
    drive_speed(speed_left, speed_right);
}

void drive_off() 
{
    drive_speed(0, 0);
}

void drive_mm(int mm)
{
    int ticks = mm / 3.25;
    drive_goto(ticks, ticks);
}

void init_robot()
{
    drive_setAcceleration(0, 150);
    drive_setAcceleration(1, 600);
    
    low(PIN_LASER);
    high(PIN_FLYWHEELS);
    low(PIN_LED);
    
    shoot_motor_is_on = 0;
    servo_angle(PIN_SERVO_RELOAD, 1000);
}

void turn_on_place_relative(int angle)
{
    if (angle == 0)
    {
        return;
    }
    int ticks_left = -1.0 * angle / 180 * 53;
    int ticks_right = 1.0 * angle / 180 * 53;
    drive_goto(ticks_left, ticks_right);
}

void ask_for_dart()
{
    high(PIN_LED);
    pause(500);
    low(PIN_LED);
}


void activate_shoot_motor(int turn_on)
{
    shoot_motor_is_on = turn_on;
    set_output(PIN_FLYWHEELS, !turn_on);
}

void shoot()
{
    if (!shoot_motor_is_on) {
        activate_shoot_motor(1);
        pause(4000);
    }    
    servo_angle(PIN_SERVO_RELOAD, 100);
    pause(500);
    servo_angle(PIN_SERVO_RELOAD, 1000);
}

void activate_laser(int turn_on)
{
    set_output(PIN_LASER, turn_on);
}

void move_servo()
{
    servo_angle(PIN_SERVO_RELOAD, 500);
    pause(500);
    servo_angle(PIN_SERVO_RELOAD, 1000);
}
