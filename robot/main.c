#include "fdserial.h"
#include "simpletools.h"

#include "communication.h"
#include "robot.h"


fdserial *usb_con;
fdserial *wlan_con;


void do_action(char *string)
{
    send_string(usb_con, string, '\r');
    int params[10];
    int param_count = parse_string(string, ';', params);
    char response[50];
    create_string(response, params, param_count, ';');
    send_string(usb_con, response, '\r');
    int cmd = params[0];
    if (cmd == 1) {
        // received drive command
        drive(params[1], params[2]);
    } else if (cmd == 2) {
        // motor off
        drive_off();
    } else if (cmd == 3) {
        // activate led
        // TODO
        ask_for_dart();
    } else if (cmd == 4) {
        // shoot
        shoot();
    } else if (cmd == 5) {
        // activate/deactivate laser
        activate_laser(params[1]);
    } else if (cmd == 6) {
        // shoot motor on
        activate_shoot_motor(params[1]);
    } else if (cmd == 7) {
        move_servo();
    } else {
        send_string(usb_con, "Wrong command", '\r');
    }
}


int main(int argc, char **argv)
{
  
    wlan_con = fdserial_open(8, 7, 0, 115200);
    usb_con = fdserial_open(31, 30, 0, 115200);
    send_string(usb_con, "Connections opened", '\r');

    init_robot();
    send_string(usb_con, "Initialized robot", '\r');

    char string[100];
    while (1)
    {
        receive_string(wlan_con, string, '\n');
        do_action(string);
    }
}
