class EthicalAIClient:
    """
    Classe responsável por abstrair a comunicação com a API de IA (Gemini, OpenAI, etc).
    Respeita o Princípio da Responsabilidade Única (SRP).
    """
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        # Aqui você inicializa o SDK da IA que for utilizar

    def generate_initial_scenario(self) -> str:
        """Busca o primeiro dilema ético para iniciar a aplicação."""
        
        # =====================================================================
        # ÁREA DE INCLUSÃO DA API (CENÁRIO INICIAL)
        # =====================================================================
        # prompt = "Gere um dilema ético complexo envolvendo tecnologia e sociedade. Máximo de 3 linhas."
        # resposta = api.generate_text(prompt)
        # return resposta
        
        return "[Área de API] - O texto gerado pela IA para o primeiro dilema aparecerá aqui."

    def generate_consequence(self, previous_scenario: str, choice: bool) -> str:
        """Gera a consequência com base no cenário anterior e na escolha (Sim/Não)."""
        
        escolha_texto = "SIM" if choice else "NÃO"
        
        # =====================================================================
        # ÁREA DE INCLUSÃO DA API (CONSEQUÊNCIA DINÂMICA)
        # =====================================================================
        # prompt = f"O cenário era: '{previous_scenario}'. O usuário escolheu: {escolha_texto}. " \
        #          f"Gere a consequência narrativa dessa escolha e apresente um novo desdobramento " \
        #          f"ético que exija um novo Sim ou Não."
        # resposta = api.generate_text(prompt)
        # return resposta
        
        return f"[Área de API] - A IA avaliará o cenário anterior e a escolha '{escolha_texto}' para gerar a próxima consequência e o novo dilema."