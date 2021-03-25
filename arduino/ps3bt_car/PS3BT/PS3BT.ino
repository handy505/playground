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



#define SENSITIVE 3

#define IN1_PIN 2
#define IN2_PIN 3
#define IN3_PIN 4
#define IN4_PIN 7
#define ENA_PIN 5
#define ENB_PIN 6


unsigned long timebase = 0;
unsigned char lefttarget = 0;
unsigned char leftpwm = 0;
unsigned char righttarget = 0;
unsigned char rightpwm = 0;
unsigned long leftstop_timestamp = 0;
unsigned long rightstop_timestamp = 0;


unsigned int calc_pwm(unsigned int value){
  int delta = 0;
  if (value > 128)      delta = value - 128;
  else if(value < 127)  delta = 127 - value;
  return delta * 2;
}

void left_forward(void){
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);  
}

void left_backward(void){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
}

void left_stop(void){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}

void right_forward(void){
  digitalWrite(IN3_PIN, HIGH);
  digitalWrite(IN4_PIN, LOW);    
}

void right_backward(void){
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, HIGH);  
}

void right_stop(void){
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);  
}

void polling(void){

  if (PS3.PS3Connected || PS3.PS3NavigationConnected) {

    int left = PS3.getAnalogHat(LeftHatY);
    int right = PS3.getAnalogHat(RightHatY);

    bool active = false;
    
    if (left < (127 - SENSITIVE)){
      // left forward
      left_forward();
      
      lefttarget = calc_pwm(left);
      if (leftpwm > lefttarget) leftpwm--;
      else                      leftpwm++;
      analogWrite(ENA_PIN, leftpwm);
      active = true;
      
    }else if (left > (127 + SENSITIVE)){
      // left backward
      left_backward();
      
      lefttarget = calc_pwm(left);
      if (leftpwm > lefttarget) leftpwm--;
      else                      leftpwm++;
      analogWrite(ENA_PIN, leftpwm);
      active = true;
      
    }else{
      left_stop();
      if(leftpwm > 20)      leftpwm -= 3;
      else if(leftpwm > 0)  leftpwm -= 1;
      analogWrite(ENA_PIN, leftpwm);
      
    }

    if (right < (127 - SENSITIVE)){
      // right forward
      right_forward();
      
      righttarget = calc_pwm(right);
      if (rightpwm > righttarget) rightpwm--;
      else                        rightpwm++;
      analogWrite(ENB_PIN, rightpwm); 
      active = true;
            
    }else if (right > (127 + SENSITIVE)){
      // right backward
      right_backward();
      
      righttarget = calc_pwm(right);
      if (rightpwm > righttarget) rightpwm--;
      else                        rightpwm++;
      analogWrite(ENB_PIN, rightpwm); 
      active = true;
      
    }else{
      right_stop();
      if(rightpwm > 20)      rightpwm -= 3;
      else if(rightpwm > 0)  rightpwm -= 1;
      analogWrite(ENB_PIN, rightpwm);
            
    }


    if (active){
      Serial.print(F("\r\n "));
      Serial.print(leftpwm); 
      Serial.print(F("\t "));
      Serial.print(rightpwm); 
      active = false;  
    }
    
  }
}

//-----------------------------
void setup() {
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);
  pinMode(ENA_PIN, OUTPUT);
  pinMode(ENB_PIN, OUTPUT);
  
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

}
