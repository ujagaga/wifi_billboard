#include <SoftwareSerial.h>

#define UART_TX_PIN             (4)
#define BTN_1_PIN               (0)
#define BTN_2_PIN               (1) /* Built in LED on GND. Need to connect to VCC, so reversed logic. */
#define BTN_3_PIN               (2)
#define BTN_4_PIN               (3)

#define UPDATE_TIMEOUT          (100)
#define MSG_START               (0xA5)

SoftwareSerial mySerial(255, UART_TX_PIN); // RX, TX

uint32_t updateTime = 0;

uint8_t btn_test(){
  uint8_t pressed = 0;
  if(digitalRead(BTN_1_PIN) == LOW){
    pressed += 1;
  }
  if(digitalRead(BTN_2_PIN) == HIGH){
    pressed += 2;
  }
  if(digitalRead(BTN_3_PIN) == LOW){
    pressed += 4;
  }
  if(digitalRead(BTN_4_PIN) == LOW){
    pressed += 8;
  }

  return pressed;

}

void setup(){
  mySerial.begin(115200);
  mySerial.write((uint8_t)MSG_START);
  mySerial.write((uint8_t)0); 

  pinMode(BTN_1_PIN, INPUT_PULLUP);
  pinMode(BTN_2_PIN, INPUT);
  pinMode(BTN_3_PIN, INPUT_PULLUP);
  pinMode(BTN_4_PIN, INPUT_PULLUP);
}

void loop(){
  if((millis() - updateTime) > UPDATE_TIMEOUT){
    uint8_t press_1 = btn_test();
    uint8_t press_2 = btn_test();
    uint8_t press_3 = btn_test();

    if((press_1 == press_2 == press_3) && (press_1 > 0)){
      mySerial.write((uint8_t)MSG_START);
      mySerial.write(press_1); 
    }    

    while(press_1 > 0){
      delay(10);
      press_1 = btn_test();      
    }

    updateTime = millis();
  }
  
}