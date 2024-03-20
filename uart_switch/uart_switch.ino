#include <SoftwareSerial.h>

#define UART_TX_PIN             (4)
#define BTN_1_PIN               (0)
#define BTN_2_PIN               (1)
#define ENC_PIN_A               (2)
#define ENC_PIN_B               (3)

#define UPDATE_TIMEOUT          (2)
#define MSG_START               (0xA5)
// Define movement type
#define DIR_IDLE             (0)
#define DIR_FWD              (1)
#define DIR_BACK             (2)

SoftwareSerial mySerial(255, UART_TX_PIN); // RX, TX

uint32_t updateTime = 0;
uint8_t btn_1_pressed = 0;
uint8_t btn_2_pressed = 0;
uint8_t old_value = 0;

void button_test(){
  btn_1_pressed = 0;
  btn_2_pressed = 0;

  int b1_state = 0;
  int b2_state = 0;

  do{  
    b1_state = digitalRead(BTN_1_PIN);
    if(b1_state){
      btn_1_pressed = 1;
    }

    b2_state = digitalRead(BTN_2_PIN);
    if(b2_state){
      btn_2_pressed = 1;
    }
  }while(b1_state || b2_state);
}

uint8_t read_enc_pins(){
   uint8_t value = digitalRead(ENC_PIN_A);
   value = (value << 1) + digitalRead(ENC_PIN_B);
   return (value & 0b11);
}

uint8_t get_enc_dir(){
  uint8_t val = read_enc_pins();
  uint8_t direction = DIR_IDLE;
  
  if(old_value != val){
    if(val == 0){
      if(old_value == 2){
        direction = DIR_FWD;
      }else{
        direction = DIR_BACK;
      }
    }else if(val == 1){
      if(old_value == 0){
        direction = DIR_FWD;
      }else{
        direction = DIR_BACK;
      }
    }else if(val == 2){
      if(old_value == 3){
        direction = DIR_FWD;
      }else{
        direction = DIR_BACK;
      }
    }else{
      if(old_value == 1){
        direction = DIR_FWD;
      }else{
        direction = DIR_BACK;
      }
    }  

    old_value = val; 
  }

  return direction;
}

void setup(){
  mySerial.begin(115200);

  pinMode(BTN_1_PIN, INPUT);
  pinMode(BTN_2_PIN, INPUT);
  pinMode(ENC_PIN_A, INPUT_PULLUP);
  pinMode(ENC_PIN_B, INPUT_PULLUP);

  old_value = read_enc_pins();
}

void loop(){
  if((millis() - updateTime) > UPDATE_TIMEOUT){
    button_test();
    uint8_t encDir = get_enc_dir();

    if(btn_1_pressed || btn_2_pressed || encDir){
      mySerial.write(MSG_START);
      mySerial.write(btn_1_pressed);
      mySerial.write(btn_2_pressed);
      mySerial.write(encDir);
    }

    updateTime = millis();
  }
  
}