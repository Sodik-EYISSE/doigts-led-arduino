const int leds[5] = {4, 6, 8, 10, 12};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    int n = Serial.read() - '0';
    for (int i = 0; i < 5; i++) {
      digitalWrite(leds[i], i < n ? HIGH : LOW);
    }
  }
}