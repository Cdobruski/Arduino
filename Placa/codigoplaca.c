const int luz = 8;
const int botao = 2; // constante refere-se ao digital 2

const int luz2 = 11;
const int botao2 = 5;

//estado inicial do botão

int estadoBotao = 0; 
int estadoBotao2 = 0;

void setup(){
 pinMode(luz, OUTPUT);
 pinMode(botao, INPUT);
 
 pinMode(luz2, OUTPUT);
 pinMode(botao2, INPUT); 
}

void loop(){
 estadoBotao = digitalRead(botao);
 estadoBotao2 = digitalRead(botao2);
  
 //estado do botão (pressionado [HIGH] ou não [LOW]
  
  if(estadoBotao == HIGH){
   digitalWrite(luz, HIGH); 
   delay(1200); //Tempo que o botão fica aceso 
  }else{
    digitalWrite(luz, LOW);
  }
   
  //estado do botão (pressionado [HIGH] ou não [LOW]
  
  if(estadoBotao2 == HIGH){
   digitalWrite(luz2, HIGH); 
   delay(1200); //Tempo que o botão fica aceso 
  }else{
    digitalWrite(luz2, LOW);
  }
}
