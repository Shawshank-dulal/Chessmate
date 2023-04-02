





















#include <Arduino.h>
#define USE_PCA9685_SERVO_EXPANDER
#include "ServoEasing.hpp"
int stat=0;
int takenCount=0;
String data="";
int sourceIndex=0,destinationIndex=0;
const int SERVO1_PIN = 0;
int magnetStatus=0;
int relayPin=A0;
int basePos=0,shoulderPos=0,elbowPos=0,wristPos=0;
ServoEasing base(PCA9685_DEFAULT_ADDRESS, &Wire),shoulder1(PCA9685_DEFAULT_ADDRESS, &Wire),shoulder2(PCA9685_DEFAULT_ADDRESS, &Wire),elbow(PCA9685_DEFAULT_ADDRESS, &Wire),wrist(PCA9685_DEFAULT_ADDRESS, &Wire);
int servoAngles[64][4]={
{104,75,130,50},
{117,63,104,59},
{114,56,85,52},
{108,51,71,46},
{110,44,55,41},
{100,39,44,35},
{94,28,30,30},
{84,22,19,33},

{99,17,15,35},
{108,27,26,33},
{114,36,37,35},
{117,44,53,39},
 {116,49,66,47},
 {121,56,78,46},
 {126,64,104,62},
 {119,71,122,69},
 
 {128,69,116,45},
{128,61,94,46},
{125,53,75,38},
{128,45,56,27},
{122,40,47,35},
{122,40,47,35},
{116,25,24,34},

{110,9,8,34},
{128,12,10,42},
{131,25,24,35},
{128,35,36,38},
{130,41,45,35},
{129,48,62,38},
{135,53,71,35},
{134,62,97,60},
{128,69,114,47},
{139,69,113,47},
{137,63,99,62},
{138,55,75,35},
{136,47,62,42},
{139,42,48,34},
{143,35,38,38},
{145,28,28,38},
{149,16,13,40},
{159,22,20,38},
{152,30,31,36},
{150,42,51,32},
{147,48,64,36},
{141,57,83,50},
{141,63,108,60},
{137,71,124,50},
{145,74,126,50},
{148,67,112,60},
{151,60,95,52},
{153,53,75,38},
{156,47,64,39},
{162,41,54,40},
{168,37,44,41},
{174,31,36,41},//8
                {180,37,45,41},
                {174,42,54,41},
                {168,45,62,38},
                {162,50,70,37},
                {158,57,82,40 },
                {154,63,104,54},
                {150,69,110,50},
                {148,75,120,50}};

void setup() {
  Serial.begin(2000000);
   pinMode(relayPin,OUTPUT);
  Wire.begin();
  wrist.attach(4,30);
  delay(500);
  
  shoulder1.attach(1,30);
  shoulder2.attach(2,150);
  delay(500);
  elbow.attach(3,50);
  delay(500);
  base.attach(SERVO1_PIN, 150);
}

void loop() {
  
  
  
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    if(stat==0){
      Serial.println(stat);
      sourceIndex=findIndex(data)-1;
      destinationIndex=findIndex(String(data[2])+String(data[3]))-1;
      Serial.println(data+":"+sourceIndex+":"+destinationIndex);
      basePos=servoAngles[sourceIndex][0];
      shoulderPos=servoAngles[sourceIndex][1];
         elbowPos=servoAngles[sourceIndex][2];
         wristPos=servoAngles[sourceIndex][3];
      moveToPos(basePos,shoulderPos,elbowPos,wristPos,30);
//    Serial.print(data);
//    Serial.print(":");
//    Serial.print(sourceIndex);
//    Serial.print(":");
//    Serial.println(destinationIndex);
      stat=1;
    }
    if(stat==1){ 
      if (data[0]=='B'){
      
        if(data[1]=='+'){
          Serial.println("Base plus");
          basePos+=1;
          
        }
        else{
          Serial.println("Base minus");
          basePos-=1;
        }
        moveBase(basePos,20);
        
      }
      else if(data[0]=='S'){
        if(data[1]=='+'){
          Serial.println("Shoulder plus");
          shoulderPos+=1;
        }
        else{
          Serial.println("Shoulder minus");
          shoulderPos-=1;
        }
        moveShoulder(shoulderPos,20);
      }
      else if(data[0]=='E'){

        if(data[1]=='+'){
          Serial.println("elbow plus");
          elbowPos+=1;
        }
        else{
          Serial.println("elbow minus");
          elbowPos-=1;
        }
        moveElbow(elbowPos,20);
      }
      else if(data[0]=='W'){
        
        
        if(data[1]=='+'){
          Serial.println("wrist plus");
          wristPos+=1;
        }
        else{
          Serial.println("wristPos minus");
          wristPos-=1;
        }
        moveWrist(wristPos,20);
       }
       if(data=="done"){
        moveToPos(123,54,116,45,30);
        Serial.println("{"+String(basePos)+","+String(shoulderPos)+","+String(elbowPos)+","+String(wristPos)+"}");
        stat=0;
       }
    }
    }
  }

int toggleMagnet(int magnetStatus){
  if(magnetStatus==0){
    Serial.println("on Magnet");
    analogWrite(relayPin,1023);
    magnetStatus=1;
//    delay(3000);
    return magnetStatus;
  }
  if(magnetStatus==1){
    delay(500);
    Serial.println("off Magnet");
    analogWrite(relayPin,0);
    magnetStatus=0;
//    delay(3000);
    return magnetStatus;
  }
}
void moveToPos(int basePos, int shoulderPos, int elbowPos,int wristPos,int moveSpeed){
  Serial.print(basePos);
  if(shoulderPos<30 ){
      moveBase(basePos,moveSpeed);
      moveShoulder(shoulderPos,moveSpeed);
        moveWrist(wristPos,moveSpeed);
          moveElbow(elbowPos,moveSpeed);
  }
  else{
    moveBase(basePos,moveSpeed);
  moveElbow(elbowPos,moveSpeed);
  moveWrist(wristPos,moveSpeed);
  moveShoulder(shoulderPos,moveSpeed);
  
  }
  magnetStatus=toggleMagnet(magnetStatus);
}
void moveBase(int angle,int servoSpeed){
  base.setSpeed(servoSpeed);
  base.easeTo(angle);
}
void moveShoulder(int angle, int servoSpeed){
  shoulder1.setSpeed(servoSpeed);
  shoulder2.setSpeed(servoSpeed);
  shoulder1.easeTo(angle);
  shoulder2.easeTo(180-angle);
}
void moveElbow(int angle, int servoSpeed){
  elbow.setSpeed(servoSpeed);
  elbow.easeTo(angle);
}
void moveWrist(int angle, int servoSpeed){
  wrist.setSpeed(servoSpeed);
  wrist.easeTo(angle);
}

void takePiece(char* pos){
  char* dest;
  dest[0]=pos[2];
  dest[1]=pos[3];
  int index=findIndex(dest);
  Serial.println("index is: "+ char(index));
  moveToPos(servoAngles[index][0],servoAngles[index][1],servoAngles[index][2],servoAngles[index][3],20);
  moveToPos( servoAngles[63][0],servoAngles[63][1]+5,servoAngles[63][2]-8,servoAngles[63][3],20);
}



void getUp(){
  int moveSpeed=15;
  moveShoulder(30,moveSpeed);
  moveElbow(55,moveSpeed);
  moveWrist(20,moveSpeed);
  moveBase(130,moveSpeed);
}

int findIndex(String data){
    if(int(data[1])%2==0){
      int a=int(data[1]-48);
      int b=int (data[0]);
      int index=8-(b-97)+(8*(a-1)) ;
      return index;     
    }
    else if(int(data[1])%2==1){
        int a=int(data[1]-48);
        int b=int(data[0]-96);
        int index=8*(a-1)+b;
//        Serial.println(a);
//        int index=8*(8-(8-48-int(data[1])-1))+(int(data[0])-96);
//        Serial.println(index);
        return index;
    }
}
