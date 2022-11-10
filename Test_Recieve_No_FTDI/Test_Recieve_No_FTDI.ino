
void setup() {
Serial.begin(57600);
pinMode(12, OUTPUT);
}

void loop() {
 if(Serial.available() > 0)
 {
  char incoming = Serial.read();
  if(incoming == '1')
  {
    digitalWrite(12, HIGH);
  }
  else if(incoming == '0')
  {
    digitalWrite(12, LOW);
  }
 }
}
