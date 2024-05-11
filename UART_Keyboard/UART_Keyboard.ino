#include <SoftwareSerial.h>

#define BTN_PIN       3
#define UART_TX_PIN   4


SoftwareSerial mySerial(255, UART_TX_PIN);
uint8_t oldBtnPress = 0;

uint8_t read_btn_press(){
  uint8_t voltage[3] = {0};
  bool stabile_read = false;

  while(!stabile_read){
    voltage[2] = voltage[1];
    voltage[1] = voltage[0];

    int adc_voltage = analogRead(BTN_PIN);
    voltage[0] = (uint8_t)(adc_voltage / 4);

    stabile_read = (voltage[0] == voltage[1]) && (voltage[2] == voltage[1]);
  } 

  if(voltage[0] > 190){
    return 0xff;
  }else if(voltage[0] > 179){
    return 0;
  }else if(voltage[0] > 168){
    return 1;
  }else if(voltage[0] > 140){
    return 2;
  }else if(voltage[0] > 50){
    return 3;
  }else{
    return 4;
  }

}

void setup() {
  mySerial.begin(9600);
  pinMode(BTN_PIN, INPUT); 
}

void loop() {
  uint8_t btnPressed = read_btn_press();
 
  if(oldBtnPress != btnPressed){
    mySerial.write(btnPressed);
    oldBtnPress = btnPressed; 
  }
}
