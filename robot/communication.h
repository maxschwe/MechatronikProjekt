#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include "fdserial.h"

void receive_string(fdserial *serial_con, char *string, char end_char);
int parse_string(char *string, char delimeter, int *params);
void send_string(fdserial *serial, char *string, char end_char);
void send_string_with_val(fdserial *serial, char *string, char end_char, int val);
void create_string(char *created_string, int *int_params, int param_count, char delimeter);

#endif
