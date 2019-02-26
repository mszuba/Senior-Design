//---ARDUINO MEGA PINOUT---
const int AZ_ACCEL = A0;
const int EL_ACCEL = A1;
const int AZ_POT = A2;
const int EL_POT = A3;
const int PULSE_PLUS = 2;
const int PULSE_MINUS = 3;
const int DIRECTION_PLUS = 4;
const int DIRECTION_MINUS = 5;
const int AZ_SWITCH_RIGHT= 6;
const int AZ_SWITCH_LEFT = 7;
const int EL_SWITCH_BOTTOM = 8;
const int EL_SWITCH_TOP = 9;

//---OTHER VARIABLES---
int count = 0;

void setup() {
  //---SET UP PINMODES---
  pinMode(PULSE_PLUS, OUTPUT);
  pinMode(PULSE_MINUS, OUTPUT);
  pinMode(AZ_SWITCH_RIGHT, INPUT);
  pinMode(AZ_SWITCH_LEFT, INPUT);
  pinMode(EL_SWITCH_BOTTOM, INPUT);
  pinMode(EL_SWITCH_TOP, INPUT);

  //---START SERIAL CONNECTION---
  Serial.begin(9600);
}

void loop() {
  //---RUN MAIN CODE HERE---
  Serial.print(count);
  count++;
  delay(100);
}
