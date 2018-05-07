/*
 Example sketch for the PS3 Bluetooth library - developed by Kristian Lauszus
 For more information visit my blog: http://blog.tkjelectronics.dk/ or
 send me an e-mail:  kristianl@tkjelectronics.com
 */

#include <PS3BT.h>
#include <usbhub.h>


// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

USB Usb;
//USBHub Hub1(&Usb); // Some dongles have a hub inside

BTD Btd(&Usb); // You have to create the Bluetooth Dongle instance like so
/* You can create the instance of the class in two ways */
PS3BT PS3(&Btd); // This will just create the instance
//PS3BT PS3(&Btd, 0x00, 0x15, 0x83, 0x3D, 0x0A, 0x57); // This will also store the bluetooth address - this can be obtained from the dongle when running the sketch

bool printTemperature, printAngle;

#define SENSITIVE 3

int leftwheel = 0;
int rightwheel = 0;
unsigned char leftpwm = 0;
unsigned char rightpwm = 0;
unsigned long timebase = 0;
unsigned long leftstop_timestamp = 0;
unsigned long rightstop_timestamp = 0;

unsigned char calc_pwm(unsigned long last_timestamp){
  int diff = (millis() - last_timestamp) / 4;
  if (diff > 255) return 255;
  else            return diff;
}

void polling(void){

  if (PS3.PS3Connected || PS3.PS3NavigationConnected) {

    int left = PS3.getAnalogHat(LeftHatY);
    if (left < (127 - SENSITIVE)){
      // left forward
      leftpwm = calc_pwm(leftstop_timestamp);
      Serial.print(F("\r\n left forward: "));
      Serial.print(leftpwm);
    }else if (left > (127 + SENSITIVE)){
      // left backward
      leftpwm = calc_pwm(leftstop_timestamp);
      Serial.print(F("\r\n left backward: "));
      Serial.print(leftpwm);      
      
    }else{
      // left stop
      leftstop_timestamp = millis();
      if (leftpwm > 2){
        leftpwm -= 2;
        Serial.print(F("\r\n left forward: "));
        Serial.print(leftpwm);
      }else{
        leftpwm = 0;  
      }
      
    }

    int right = PS3.getAnalogHat(RightHatY);
    if (right < (127 - SENSITIVE)){
      // right forward
      rightpwm = calc_pwm(rightstop_timestamp);
      Serial.print(F("\r\n right forward: "));
      Serial.print(rightpwm); 
            
    }else if (right > (127 + SENSITIVE)){
      // right backward
      rightpwm = calc_pwm(rightstop_timestamp);
      Serial.print(F("\r\n right backward: "));
      Serial.print(rightpwm); 
      
    }else{
      // right stop
      rightstop_timestamp = millis();
      if (rightpwm > 2){
        rightpwm -= 2 ;
        Serial.print(F("\r\n right forward: "));
        Serial.print(rightpwm);
      }else{
        rightpwm = 0;  
      }
      
      
    }  
  }
}
//-----------------------------
void setup() {
  Serial.begin(115200);
#if !defined(__MIPSEL__)
  while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
  if (Usb.Init() == -1) {
    Serial.print(F("\r\nOSC did not start"));
    while (1); //halt
  }
  Serial.print(F("\r\nPS3 Bluetooth Library Started"));

  timebase = millis();
  
}

//-----------------------------
void loop() {
  Usb.Task();

  if (millis() - timebase > 10){
    
    polling();
    
    timebase = millis();  
  }



#if 0 // Set this to 1 in order to see the angle of the controller
    if (printAngle) {
      Serial.print(F("\r\nPitch: "));
      Serial.print(PS3.getAngle(Pitch));
      Serial.print(F("\tRoll: "));
      Serial.print(PS3.getAngle(Roll));
    }
#endif

}
