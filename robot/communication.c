#include "communication.h"

void receive_string(fdserial *serial_con, char *string, char end_char)
{
  int index = 0;
  char new_char;
  while ((new_char = fdserial_rxChar(serial_con)) != end_char)
  {
    string[index++] = new_char;
  }
  string[index] = '\0';
}

void send_string(fdserial *serial_con, char *string, char end_char)
{
  char c;
  int index = 0;
  while ((c = string[index++]) != '\0')
  {
    fdserial_txChar(serial_con, c);
  }
  fdserial_txChar(serial_con, end_char);
}

void send_string_with_val(fdserial *serial, char *string, char end_char, int val)
{
  char c;
  int index = 0;
  while ((c = string[index++]) != '\0')
  {
    fdserial_txChar(serial, c);
  }
  if (val < 0)
  {
    fdserial_txChar(serial, '-');
    val = -1 * val;
  }
  if (val == 0)
  {
    fdserial_txChar(serial, '0');
  }
  int divider = 10000;
  while (divider >= 1)
  {
    int digit = val / divider;
    char val_char = digit + '0';
    val -= digit * divider;
    divider /= 10;
    fdserial_txChar(serial, val_char);
  }
  fdserial_txChar(serial, end_char);
}

int parse_string(char *string, char delimeter, int *params)
{
  char c;
  int i = 0;
  int param_count = 1;
  while ((c = string[i++]) != '\0')
  {
    if (c == delimeter)
    {
      param_count++;
    }
  }
  i = 0;
  for (int param_index = 0; param_index < param_count; ++param_index)
  {
    int param_is_negative = string[i] == '-';
    int value = 0;
    if (param_is_negative)
    {
      i++;
    }
    while ((c = string[i++]) != delimeter && c != '\0')
    {
      value = value * 10 + c - '0';
    }
    if (param_is_negative)
    {
      value *= -1;
    }
    params[param_index] = value;
  }
  return param_count;
}

void create_string(char *created_string, int *int_params, int param_count, char delimeter)
{
  int string_length = 0;
  for (int i = 0; i < param_count; i++)
  {
    int param = int_params[i];
    int abs_param;
    if (param < 0)
    {
      abs_param = -param;
      string_length += 1;
    }
    else
    {
      abs_param = param;
    }
    int temp = abs_param;
    do
    {
      string_length += 1;
    } while (temp = temp / 10);
  }
  string_length += param_count;

  int i = string_length - 1;
  created_string[i--] = '\0';
  for (int j = param_count - 1; j >= 0; --j)
  {
    int param = int_params[j];
    int is_negative = param < 0;
    if (is_negative)
    {
      param = -param;
    }
    do
    {
      char next_char = param % 10 + '0';
      created_string[i--] = next_char;
    } while ((param = param / 10) > 0);
    if (is_negative)
    {
      created_string[i--] = '-';
    }
    created_string[i--] = delimeter;
  }
}