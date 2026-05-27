import os
from google import genai
from dotenv import load_dotenv

class EthicalAIClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no .env")
        
        # O novo SDK utiliza a classe Client
        self.client = genai.Client(api_key=api_key)
        
        # Com a nova biblioteca, podemos usar o modelo flash mais atual diretamente
        self.model_id = 'gemini-2.5-flash'
        print(f"[Sistema] Cliente IA inicializado com o modelo: {self.model_id}")

    def generate_initial_scenario(self) -> str:
        # Seu prompt customizado para a primeira pergunta
        prompt = (
            "Você é um contador de histórias de teste ético. "
            "Quero que crie uma pergunta que questione a ética entre o que seria mais ou menos aceitável de acordo com a sociedade atual. "
            "Use uma linguagem mais comum em que pessoas mais simples consigam ler sem problemas. "
            "Use de exemplo para criação de novos dilemas o famoso dilema da alavanca no trilho do trem para direcionar a uma pessoa ou várias. Esse é o nível de perguntas que quero, não necessáriamente relacionados a um trem "
            "Ela tem que (obrigatoriamente) ser uma pergunta que pode ser respondida apenas com sim, ou com não. "
            "Não responda a esse prompt como se estivesse respondendo alguém."
            "Preferencialmente textos curtos."
        )
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text

    def generate_consequence(self, previous_scenario: str, user_choice: bool, is_final: bool = False) -> str:
        choice_text = "SIM" if user_choice else "NÃO"
        
        if is_final:
            # Prompt para quando o usuário chegar na 5ª rodada (Encerramento)
            prompt = (
                f"O cenário anterior era: '{previous_scenario}'. A decisão final do usuário foi: {choice_text}.\n\n"
                "Esta é a última rodada. Descreva a consequência direta (positiva ou negativa) dessa decisão e encerre a história com uma "
                "conclusão moral reflexiva baseada nas escolhas que ele fez ao longo do teste. "
                "NÃO crie um novo dilema e NÃO faça perguntas. Apenas texto limpo, sem markdown. "
                "Preferencialmente textos curtos."
            )
        else:
           # Seu prompt customizado para as rodadas intermediárias (Novos dilemas)
            prompt = (
                f"O cenário anterior era: '{previous_scenario}'.\n"
                f"A decisão do usuário foi: {choice_text}.\n\n"
                "Com base nessa decisão, descreva a consequência direta (positiva ou negativa). "
                "PULE DUAS LINHAS e imediatamente apresente um NOVO desdobramento ou dilema ético diferente do anterior e sem relação alguma ao mesmo. "
                "Lembre-se que tem que ser um dilema que exija um novo SIM ou NÃO. Seja direto e não use formatação markdown, "
                "apenas texto limpo. Preferencialmente textos curtos."
            )
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text