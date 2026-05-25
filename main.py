import utime
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

from bmp085 import BMP180
import time

I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 101325

def greeting():
    
    lcd.clear()
    lcd.move_to(4,0)
    lcd.putstr("PeterZig")
    lcd.move_to(3,1)
    lcd.putstr("15-05-2026")
    utime.sleep(2)
    lcd.clear()
    

def read_temp():
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.2f}".format(temperature)
    string_temperature = str(formatted_temperature)
    print(string_temperature)
    utime.sleep(2)
    return string_temperature


def customcharacter():
    
  #arrow     
  lcd.custom_char(0, bytearray([
    0x04,
  0x0E,
  0x15,
  0x04,
  0x04,
  0x04,
  0x04,
  0x04
        
        ]))
  
  
  #cloud
  lcd.custom_char(1, bytearray([
    0x00,
  0x00,
  0x0A,
  0x1F,
  0x1F,
  0x0A,
  0x14,
  0x00
        
        ]))
  
  #temp
  lcd.custom_char(2, bytearray([
   0x04,
  0x04,
  0x04,
  0x04,
  0x0A,
  0x11,
  0x1F,
  0x0E
        ]))
  
    #celcius
  lcd.custom_char(3, bytearray([
  0x0E,
  0x0A,
  0x0E,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00
        ]))

greeting()
customcharacter()

while True:
    lcd.move_to(0,0)
    temperature = read_temp()
    lcd.putchar(chr(2))
    lcd.putstr(temperature)
    lcd.putchar(chr(3))
    lcd.putstr("C")
    pres_hPa = bmp.pressure
    altitude = abs(bmp.altitude)
    print(altitude)
    print(pres_hPa)
    lcd.move_to(9,0)
    lcd.putchar(chr(0))
    lcd.putstr(str(altitude))
    lcd.move_to(15,0)
    lcd.putstr("m")
    lcd.move_to(0,1)
    lcd.putchar(chr(1))
    lcd.move_to(1,1)
    lcd.putstr(str(pres_hPa))
    lcd.move_to(8,1)
    lcd.putstr("hPa")
