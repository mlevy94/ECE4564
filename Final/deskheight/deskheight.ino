// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  int sensorValue = 0;
  int sensorAvg = 0;
  // get 10 reads and average them out
  for (int i = 0; i < 10; i++) {
    sensorAvg += analogRead(A0);
    delay(25);
  }
  sensorValue = sensorAvg / 10;
  Serial.println(sensorValue);
}
