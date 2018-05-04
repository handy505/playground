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
unsigned long timebase = 0;
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

  if (millis() - timebase > 100){
    if(leftwheel > 60){
      leftwheel -= 50;  
    }else if (leftwheel < -60){
      leftwheel += 50;  
    }

    if(rightwheel > 60){
      rightwheel -= 50;  
    }else if (rightwheel < -60){
      rightwheel += 50;  
    }
    Serial.print(F("\r\n status: "));
    Serial.print(leftwheel);
    Serial.print(F("\t"));
    Serial.print(rightwheel);
    Serial.print(F("\r\n"));
    
    timebase = millis();  
  }

  if (PS3.PS3Connected || PS3.PS3NavigationConnected) {
    if (PS3.getAnalogHat(LeftHatX) > (127 + SENSITIVE) 
    ||  PS3.getAnalogHat(LeftHatX) < (127 - SENSITIVE) 
    ||  PS3.getAnalogHat(LeftHatY) > (127 + SENSITIVE) 
    ||  PS3.getAnalogHat(LeftHatY) < (127 - SENSITIVE) 
    ||  PS3.getAnalogHat(RightHatX) > (127 + SENSITIVE) 
    ||  PS3.getAnalogHat(RightHatX) < (127 - SENSITIVE) 
    ||  PS3.getAnalogHat(RightHatY) > (127 + SENSITIVE) 
    ||  PS3.getAnalogHat(RightHatY) < (127 - SENSITIVE) ) {

      int lefty = PS3.getAnalogHat(LeftHatY);
      int righty = PS3.getAnalogHat(RightHatY);

      
      //Serial.print(F("\r\nLeftHatX: "));
      //Serial.print(PS3.getAnalogHat(LeftHatX));
      //Serial.print(F("\r\nLeftHatY: "));
      //Serial.print(PS3.getAnalogHat(LeftHatY));
      //Serial.print(lefty);

      
      if (PS3.PS3Connected) { // The Navigation controller only have one joystick
        //Serial.print(F("\tRightHatX: "));
        //Serial.print(PS3.getAnalogHat(RightHatX));
        //Serial.print(F("\tRightHatY: "));
        //Serial.print(PS3.getAnalogHat(RightHatY));
        //Serial.print(righty);
      }


      int acc = 255 - lefty - 127;
      leftwheel += acc;
      if (leftwheel > 30000){
        leftwheel = 30000;
      }else if (leftwheel < -30000){
        leftwheel = -30000;
      }
      
      acc = 255 - righty - 127;
      rightwheel += acc;
      if (rightwheel > 30000){
        rightwheel = 30000;
      }else if (rightwheel < -30000){
        rightwheel = -30000;
      }
      /*
      Serial.print(F("\r\n status: "));
      Serial.print(leftwheel);
      Serial.print(F("\t"));
      Serial.print(rightwheel);
      Serial.print(F("\r\n"));*/
      
    }

    // Analog button values can be read from almost all buttons
    if (PS3.getAnalogButton(L2) || PS3.getAnalogButton(R2)) {
      Serial.print(F("\r\nL2: "));
      Serial.print(PS3.getAnalogButton(L2));
      if (PS3.PS3Connected) {
        Serial.print(F("\tR2: "));
        Serial.print(PS3.getAnalogButton(R2));
      }
    }

    if (PS3.getButtonClick(PS)) {
      Serial.print(F("\r\nPS"));
      PS3.disconnect();
    }
    else {
      if (PS3.getButtonClick(TRIANGLE)) {
        Serial.print(F("\r\nTraingle"));
        PS3.setRumbleOn(RumbleLow);
      }
      if (PS3.getButtonClick(CIRCLE)) {
        Serial.print(F("\r\nCircle"));
        PS3.setRumbleOn(RumbleHigh);
      }
      if (PS3.getButtonClick(CROSS))
        Serial.print(F("\r\nCross"));
      if (PS3.getButtonClick(SQUARE))
        Serial.print(F("\r\nSquare"));

      if (PS3.getButtonClick(UP)) {
        Serial.print(F("\r\nUp"));
        if (PS3.PS3Connected) {
          PS3.setLedOff();
          PS3.setLedOn(LED4);
        }
      }
      if (PS3.getButtonClick(RIGHT)) {
        Serial.print(F("\r\nRight"));
        if (PS3.PS3Connected) {
          PS3.setLedOff();
          PS3.setLedOn(LED1);
        }
      }
      if (PS3.getButtonClick(DOWN)) {
        Serial.print(F("\r\nDown"));
        if (PS3.PS3Connected) {
          PS3.setLedOff();
          PS3.setLedOn(LED2);
        }
      }
      if (PS3.getButtonClick(LEFT)) {
        Serial.print(F("\r\nLeft"));
        if (PS3.PS3Connected) {
          PS3.setLedOff();
          PS3.setLedOn(LED3);
        }
      }

      if (PS3.getButtonClick(L1))
        Serial.print(F("\r\nL1"));
      if (PS3.getButtonClick(L3))
        Serial.print(F("\r\nL3"));
      if (PS3.getButtonClick(R1))
        Serial.print(F("\r\nR1"));
      if (PS3.getButtonClick(R3))
        Serial.print(F("\r\nR3"));

      if (PS3.getButtonClick(SELECT)) {
        Serial.print(F("\r\nSelect - "));
        PS3.printStatusString();
      }
      if (PS3.getButtonClick(START)) {
        Serial.print(F("\r\nStart"));
        printAngle = !printAngle;
      }
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
#if 0 // Set this to 1 in order to enable support for the Playstation Move controller
  else if (PS3.PS3MoveConnected) {
    if (PS3.getAnalogButton(T)) {
      Serial.print(F("\r\nT: "));
      Serial.print(PS3.getAnalogButton(T));
    }
    if (PS3.getButtonClick(PS)) {
      Serial.print(F("\r\nPS"));
      PS3.disconnect();
    }
    else {
      if (PS3.getButtonClick(SELECT)) {
        Serial.print(F("\r\nSelect"));
        printTemperature = !printTemperature;
      }
      if (PS3.getButtonClick(START)) {
        Serial.print(F("\r\nStart"));
        printAngle = !printAngle;
      }
      if (PS3.getButtonClick(TRIANGLE)) {
        Serial.print(F("\r\nTriangle"));
        PS3.moveSetBulb(Red);
      }
      if (PS3.getButtonClick(CIRCLE)) {
        Serial.print(F("\r\nCircle"));
        PS3.moveSetBulb(Green);
      }
      if (PS3.getButtonClick(SQUARE)) {
        Serial.print(F("\r\nSquare"));
        PS3.moveSetBulb(Blue);
      }
      if (PS3.getButtonClick(CROSS)) {
        Serial.print(F("\r\nCross"));
        PS3.moveSetBulb(Yellow);
      }
      if (PS3.getButtonClick(MOVE)) {
        PS3.moveSetBulb(Off);
        Serial.print(F("\r\nMove"));
        Serial.print(F(" - "));
        PS3.printStatusString();
      }
    }
    if (printAngle) {
      Serial.print(F("\r\nPitch: "));
      Serial.print(PS3.getAngle(Pitch));
      Serial.print(F("\tRoll: "));
      Serial.print(PS3.getAngle(Roll));
    }
    else if (printTemperature) {
      Serial.print(F("\r\nTemperature: "));
      Serial.print(PS3.getTemperature());
    }
  }
#endif
}
