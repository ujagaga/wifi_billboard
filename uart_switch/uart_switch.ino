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

void setup(){
  mySerial.begin(115200);

  pinMode(BTN_1_PIN, INPUT_PULLUP);
  pinMode(BTN_2_PIN, INPUT);
  pinMode(BTN_3_PIN, INPUT_PULLUP);
  pinMode(BTN_4_PIN, INPUT_PULLUP);
}

void loop(){
  if((millis() - updateTime) > UPDATE_TIMEOUT){
    bool btn1 = digitalRead(BTN_1_PIN);
    bool btn2 = digitalRead(BTN_2_PIN);
    bool btn3 = digitalRead(BTN_3_PIN);
    bool btn4 = digitalRead(BTN_4_PIN);

    if(!btn1){
      mySerial.write(MSG_START);
      mySerial.write(1);      
    }else if(btn2){
      mySerial.write(MSG_START);
      mySerial.write(2);      
    }else if(!btn3){
      mySerial.write(MSG_START);
      mySerial.write(3);      
    }else if(!btn4){
      mySerial.write(MSG_START);
      mySerial.write(4);      
    }

    while(btn1 || btn2 || btn3 || btn4){
      btn1 = digitalRead(BTN_1_PIN);
      btn2 = digitalRead(BTN_2_PIN);
      btn3 = digitalRead(BTN_3_PIN);
      btn4 = digitalRead(BTN_4_PIN);
      delay(100);
    }

    updateTime = millis();
  }
  
}