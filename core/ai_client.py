import google.generativeai as genai


class EthicalAIClient:
    MODEL = "gemini-2.0-flash"

    def __init__(self, api_key: str = ""):
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(self.MODEL)

    def generate_initial_scenario(self) -> str:
        prompt = (
            "Você é um narrador de dilemas éticos. Apresente um dilema ético complexo "
            "em português, curto (máximo 4 linhas), impactante e sem resposta óbvia. "
            "Envolva tecnologia, sociedade ou vida humana. "
            "Termine com uma pergunta direta que exija apenas Sim ou Não."
        )
        try:
            return self._model.generate_content(prompt).text
        except Exception as e:
            return f"Erro ao conectar com a IA: {e}"

    def generate_consequence(self, previous_scenario: str, choice: bool) -> str:
        escolha = "SIM" if choice else "NÃO"
        prompt = (
            f"Cenário: {previous_scenario}\n"
            f"Escolha feita: {escolha}\n\n"
            "Em português: descreva em até 3 linhas a consequência dramática dessa escolha. "
            "Depois apresente um novo dilema ético curto decorrente dela, "
            "que também exija uma resposta Sim ou Não."
        )
        try:
            return self._model.generate_content(prompt).text
        except Exception as e:
            return f"Erro ao conectar com a IA: {e}"
