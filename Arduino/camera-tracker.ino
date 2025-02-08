#include <AccelStepper.h>

// Define step constant
#define FULLSTEP 8


bool previousMotorState = false;
bool motorFree = true;

int rotatePosition = 0;
int tiltPosition = 0;

bool messagePrinted = false;

AccelStepper yawStepper(FULLSTEP, 4, 3, 5, 2);
AccelStepper pitchStepper1(FULLSTEP, 13, 11, 12, 10);
AccelStepper pitchStepper2(FULLSTEP, 6, 8, 7, 9);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);


  pitchStepper1.setMaxSpeed(1000.0);
	pitchStepper1.setAcceleration(50.0);
	pitchStepper1.setSpeed(200);
	

	// set the same for motor 2
	pitchStepper2.setMaxSpeed(1000.0);
	pitchStepper2.setAcceleration(50.0);
	pitchStepper2.setSpeed(200);
	

  yawStepper.setMaxSpeed(2000.0);
	yawStepper.setAcceleration(200);
	yawStepper.setSpeed(500);
	
}


void rotateToPosition(long target) {

  yawStepper.moveTo(target);

  while (yawStepper.distanceToGo() != 0) {
    yawStepper.run(); // Continuously move the motor
  } 
}

void pitchToPosition(long target) {

  pitchStepper1.moveTo(target);
  pitchStepper2.moveTo(-target);

  while (pitchStepper2.distanceToGo() != 0) {
    pitchStepper1.run();
    pitchStepper2.run(); // Continuously move the motor
    motorFree = false;
  }
}


void handleRotate(int args){
  
  rotatePosition = rotatePosition - args;
  rotateToPosition(rotatePosition);

}

void handleTilt(int args){
  if (abs(tiltPosition - args) < 500) {
    tiltPosition = tiltPosition - args;
    pitchToPosition(tiltPosition);
  }
}






void loop() {
  // put your main code here, to run repeatedly:
  previousMotorState = motorFree;

  if (pitchStepper1.distanceToGo() == 0 && motorFree == false) {
    motorFree = true;
  }
  
  if (previousMotorState == false && motorFree == true) {
    delay(1000);
    Serial.println("motor free");
  }

  if (Serial.available() > 0) {
    int message = Serial.parseInt();
    if (message != 0){
      Serial.print("You entered: ");
      Serial.println(message);
      handleRotate(message);
    }
    int message2 = Serial.parseInt();
    if (message2 != 0){
      Serial.print("You entered: ");
      Serial.println(message2);
      handleTilt(message2);
    }

  }


}
