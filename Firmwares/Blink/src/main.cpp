#include <Arduino.h>
#include <EEPROM.h>
#include "er_oled.h"


uint8_t oled_buf[WIDTH * HEIGHT / 8];
int inventory;
long cNumber;

void save_to_eeprom(long data) {
  byte four  = (data & 0xFF);
  byte three = ((data >> 8) & 0xFF);
  byte two   = ((data >> 16) & 0xFF);
  byte one   = ((data >> 24) & 0xFF);
  
  EEPROM.write(0, four);
  EEPROM.write(1, three);
  EEPROM.write(2, two);
  EEPROM.write(3, one);
}

long read_eeprom() {
  long four  = EEPROM.read(0);
  long three = EEPROM.read(1);
  long two   = EEPROM.read(2);
  long one   = EEPROM.read(3);
  
  return ((four << 0) & 0xFF) + ((three << 8) & 0xFFFF) + ((two << 16) & 0xFFFFFF) + ((one << 24) & 0xFFFFFFFF);
}

void write_c_number(){
  char longStr[13];
  snprintf(longStr, sizeof(longStr), "C%ld", cNumber);
  er_oled_string((uint8_t)(72 - (strlen(longStr) * 6))/2, 24, longStr, 12, 1, oled_buf);
}

void write_inventory(){
  char intStr[5];
  snprintf(intStr, sizeof(intStr), "%d", inventory);
  er_oled_string((uint8_t)(72 - (strlen(intStr) * 6))/2, 4, intStr, 12, 1, oled_buf);
}

void refresh_info(){
  er_oled_clear(oled_buf);
  write_c_number();
  write_inventory();
  er_oled_display(oled_buf);
}

void setup() {
  er_oled_begin();
  
  save_to_eeprom(13245678);
  cNumber = read_eeprom();
  inventory = 1000;
  refresh_info();
}

void loop() {
  //command(0xa6);
  //delay(300);
  //command(0xa7);
  //delay(300);
}

