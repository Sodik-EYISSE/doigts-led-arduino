const int leds[5] = {12, 10, 8, 6, 4};
int n = 0;                       // déclarée en haut : elle survit entre deux passages

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {
  // 1) Si un message arrive, on met à jour n et on affiche n LED
  if (Serial.available() > 0) {
    n = Serial.read() - '0';     // pas de "int" : on modifie la variable du haut
    for (int i = 0; i < 5; i++) {
      digitalWrite(leds[i], i < n ? HIGH : LOW);
    }
  }

  // 2) À chaque passage, si n vaut 5, on clignote
  if (n == 5) {
    for (int i = 0; i < 5; i++) {
      digitalWrite(leds[i], HIGH);
    }
    delay(500);
    for (int i = 0; i < 5; i++) {
      digitalWrite(leds[i], LOW);
    }
    delay(500);                  // ce 2e delay manquait
  }
}