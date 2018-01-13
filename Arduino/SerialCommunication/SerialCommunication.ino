int x,y;
const int out1PIN = 12; 
const int out2PIN = 13;

/** 
 * we want to read a Number to define state of out1 and ou2. 
 * -----------------------
 * | state | out1 | out2 |
 * -----------------------
 * |  0    | LOW  | LOW  |
 * -----------------------
 * |  1    | HIGH | LOW  |
 * -----------------------
 * |  2    | LOW  | HIGH |
 * -----------------------
 * |  3    | HIGH | HIGH |
 * -----------------------
 */
byte state = 0;


void setup() {
  pinMode(out1PIN, OUTPUT);
  pinMode(out2PIN, OUTPUT);
  Serial.begin(9600);      // open the serial port at 9600 bps:    
}

void loop() {  
  mockingBatteryStatus();

  if (Serial.available()) {
    state = Serial.read() - '0';
    setState(state);
  }
}

void setState(int s){
  switch (s){
  case 0:
    digitalWrite(out1PIN , LOW);
    digitalWrite(out2PIN , LOW);
    break; 
  case 1:
    digitalWrite(out1PIN , HIGH);
    digitalWrite(out2PIN , LOW);
    break; 
  case 2:
    digitalWrite(out1PIN , LOW);
    digitalWrite(out2PIN , HIGH);
    break; 
  case 3:
    digitalWrite(out1PIN , HIGH);
    digitalWrite(out2PIN , HIGH);
    break; 
  default:
    digitalWrite(out1PIN , LOW);
    digitalWrite(out2PIN , LOW);
    break; 
  }
  delay(1);
}

/** 
 * the final product should send Battery Info to the RasPi. Here we mocking it to validate
 * the communication between RasPi and Arduino 
 */
void mockingBatteryStatus() {
  x = rand() % (100 + 1 - 0) + 0;
  y = rand() % (100 + 1 - 0) + 0;

  Serial.print(x);       // print as an ASCII-encoded decimal - same as "DEC"
  Serial.print(" ");       // print as an ASCII-encoded decimal - same as "DEC"
  Serial.println(y);       // print as an ASCII-encoded decimal - same as "DEC"
  delay(200);            // delay 200 milliseconds
}

