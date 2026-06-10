from groq import Groq


class EthicalAIClient:
    MODEL = "llama-3.3-70b-versatile"

    def __init__(self, api_key: str = ""):
        self._client = Groq(api_key=api_key)

    def generate_initial_scenario(self) -> str:
        prompt = (
            "Você é um narrador de dilemas éticos. Apresente um dilema ético complexo "
            "em português, curto (máximo 4 linhas), impactante e sem resposta óbvia. "
            "Envolva tecnologia, sociedade ou vida humana. "
            "Termine com uma pergunta direta que exija apenas Sim ou Não."
        )
        try:
            resp = self._client.chat.completions.create(
                model=self.MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            return resp.choices[0].message.content
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
            resp = self._client.chat.completions.create(
                model=self.MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=350,
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"Erro ao conectar com a IA: {e}"
