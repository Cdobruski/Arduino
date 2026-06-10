// Componente reusável para controle de LEDs
class Led {
  private:
    uint8_t pin;
  public:
    Led(uint8_t pinNumber) : pin(pinNumber) {}
    
    void init() {
      pinMode(pin, OUTPUT);
      setOff();
    }
    
    void setOn() {
      digitalWrite(pin, HIGH);
    }
    
    void setOff() {
      digitalWrite(pin, LOW);
    }
};

// Componente reusável para leitura de Botões com Debounce e Pull-up interno
class DebouncedButton {
  private:
    uint8_t pin;
    int state;
    int lastReading;
    unsigned long lastDebounceTime;
    unsigned long debounceDelay;
    
  public:
    DebouncedButton(uint8_t pinNumber, unsigned long debounceMs = 50) 
      : pin(pinNumber), debounceDelay(debounceMs), state(HIGH), lastReading(HIGH), lastDebounceTime(0) {}

    void init() {
      // Ativa o resistor interno: pino lê HIGH quando aberto e LOW quando pressionado
      pinMode(pin, INPUT_PULLUP); 
    }

    bool update() {
      bool stateChanged = false;
      int reading = digitalRead(pin);

      if (reading != lastReading) {
        lastDebounceTime = millis();
      }

      if ((millis() - lastDebounceTime) > debounceDelay) {
        if (reading != state) {
          state = reading;
          stateChanged = true;
        }
      }

      lastReading = reading;
      return stateChanged;
    }

    bool isPressed() {
      // Retorna true quando o pino é conectado ao GND (LOW)
      return state == LOW;
    }
};

// Instanciação dos componentes com as portas atuais
Led luz1(8);
DebouncedButton botao1(2);

Led luz2(11);
DebouncedButton botao2(5);

void setup() {
  luz1.init();
  botao1.init();
  
  luz2.init();
  botao2.init();

  Serial.begin(9600);
  delay(1000);
  Serial.println("ARDUINO_READY");
}

void loop() {
  // Execução do Módulo 1 (Pino 2 -> Pino 8)
  if (botao1.update()) {
    if (botao1.isPressed()) {
      luz1.setOn();
      Serial.println("BUTTON1:HIGH");
    } else {
      luz1.setOff();
    }
  }

  // Execução do Módulo 2 (Pino 5 -> Pino 11)
  if (botao2.update()) {
    if (botao2.isPressed()) {
      luz2.setOn();
      Serial.println("BUTTON2:HIGH");
    } else {
      luz2.setOff();
    }
  }
}