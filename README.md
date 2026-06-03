<h1 align="center">
  ⚖️ Dilemas Éticos: IA & Hardware Engine
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white" alt="Arduino">
  <img src="https://img.shields.io/badge/AI_Ready-BB86FC?style=for-the-badge&logo=openai&logoColor=white" alt="AI Ready">
</p>

<p align="center">
  Uma engine de narrativa ramificada interativa, construída para explorar consequências morais por meio da integração de hardware (Arduino), IA e uma interface gráfica fluida.
</p>

---

## 📌 Índice
* [Sobre o Projeto](#-sobre-o-projeto)
* [Arquitetura & Clean Code](#-arquitetura--clean-code)
* [Interface e UX](#-interface-e-ux)
* [Como Executar](#-como-executar)
* [Integração Futura (Roadmap)](#-integração-futura-roadmap)

---

## 📖 Sobre o Quick Choice Idea
Este sistema apresenta ao usuário cenários éticos complexos onde não há saída neutra — apenas decisões binárias de **SIM** ou **NÃO**. Foi projetado para demonstrar o fluxo de dados em tempo real entre um microcontrolador (sensor/gatilho) e uma aplicação Python local, alimentada por IA.

### ✨ Principais Funcionalidades
- **Árvore de decisão dinâmica:** respostas moldam o próximo cenário instantaneamente.
- **Isolamento de hardware:** camada dedicada para leitura serial assíncrona, evitando travamentos na interface.
- **IA generativa (plug & play):** arquitetura pronta para conectar APIs de geração de texto (LLMs).

---

## ⚙️ Arquitetura & Clean Code
O projeto segue princípios de separação de responsabilidades, mantendo a visão (View), a lógica (Controller) e a integração externa (Hardware/AI) bem isoladas.

<details>
<summary><b>📂 Estrutura de Diretórios</b></summary>
<br>

```text
Arduino/
├── core/
│   ├── ai_client.py
│   └── data_parser.py
├── hardware/
│   └── serial_client.py
├── ui/
│   └── main_window.py
├── Placa/
│   └── codigoplaca.c
├── config.json
├── requirements.txt
├── README.md
└── main.py
```
</details>

---

## 🚀 Como Executar

1. Instale as dependências do Python:
   ```bash
   pip install -r requirements.txt
   ```
2. Ajuste a porta serial em `config.json` para a COM correta do Arduino.
3. Carregue o firmware em `Placa/codigoplaca.c` para o Arduino.
4. Execute o programa Python:
   ```bash
   python main.py
   ```

### Como o Arduino interage
- O firmware envia `BUTTON1:HIGH` quando o botão 1 é pressionado.
- O firmware envia `BUTTON2:HIGH` quando o botão 2 é pressionado.
- O Python converte esses eventos em escolhas `SIM` e `NÃO`.

---

## 📌 Integração Futura (Roadmap)
- Melhorar o tratamento de erros de serial e reconexão automática.
- Incluir suporte a outros protocolos de hardware.
- Adicionar testes unitários para o parser serial e a lógica de controle.
