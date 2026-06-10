const int luz = 8;
const int botao = 2; // constante refere-se ao digital 2

const int luz2 = 11;
const int botao2 = 5;

int estadoBotaoAnterior = LOW;
int estadoBotao2Anterior = LOW;
unsigned long ultimaMudancaBotao = 0;
unsigned long ultimaMudancaBotao2 = 0;
const unsigned long debounceDelay = 50;

void setup() {
  pinMode(luz, OUTPUT);
  pinMode(botao, INPUT);

  pinMode(luz2, OUTPUT);
  pinMode(botao2, INPUT);

  Serial.begin(9600);
  delay(1000);
  Serial.println("ARDUINO_READY");
}

void loop() {
  int leituraBotao = digitalRead(botao);
  int leituraBotao2 = digitalRead(botao2);
  unsigned long agora = millis();

  if (leituraBotao != estadoBotaoAnterior) {
    ultimaMudancaBotao = agora;
  }

  if ((agora - ultimaMudancaBotao) > debounceDelay) {
    if (leituraBotao != estadoBotaoAnterior) {
      estadoBotaoAnterior = leituraBotao;
      if (leituraBotao == HIGH) {
        digitalWrite(luz, HIGH);
        Serial.println("BUTTON1:HIGH");
      } else {
        digitalWrite(luz, LOW);
      }
    }
  }

  if (leituraBotao2 != estadoBotao2Anterior) {
    ultimaMudancaBotao2 = agora;
  }

  if ((agora - ultimaMudancaBotao2) > debounceDelay) {
    if (leituraBotao2 != estadoBotao2Anterior) {
      estadoBotao2Anterior = leituraBotao2;
      if (leituraBotao2 == HIGH) {
        digitalWrite(luz2, HIGH);
        Serial.println("BUTTON2:HIGH");
      } else {
        digitalWrite(luz2, LOW);
      }
    }
  }
}
