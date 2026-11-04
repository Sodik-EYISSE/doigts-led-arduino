const int leds[5] = {12, 10, 8, 6, 4};
int n = 0;                                  // nombre de doigts reçu
unsigned long dernierChangement = 0;        // heure du dernier changement d'état
const unsigned long INTERVALLE = 500;       // durée de chaque état (ms)
bool etatClignote = false;                  // false = éteint, true = allumé

void afficher(int nb) {                     // allume nb LED, éteint les autres
  for (int i = 0; i < 5; i++) {
    digitalWrite(leds[i], i < nb ? HIGH : LOW);
  }
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {
  // 1) Lecture de la série
  if (Serial.available() > 0) {
    int c = Serial.read();
    if (c >= '0' && c <= '5') {             // ignore les caractères parasites
      n = c - '0';
      afficher(n);
      if (n == 5) {                         // on démarre le clignotement
        etatClignote = true;
        dernierChangement = millis();
      }
    }
  }

  // 2) Clignotement non bloquant à 5 doigts
  if (n == 5) {
    unsigned long maintenant = millis();
    if (maintenant - dernierChangement >= INTERVALLE) {
      dernierChangement = maintenant;
      etatClignote = !etatClignote;
      afficher(etatClignote ? 5 : 0);
    }
  }
}