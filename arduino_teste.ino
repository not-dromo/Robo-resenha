void setup() {
  Serial.begin(115200);
  Serial.println("Arduino pronto.");

}

void loop() {
  if (Serial.available() > 0) {
    String recebido = Serial.readStringUntil('\n');
    Serial.println(recebido);
  }
}
