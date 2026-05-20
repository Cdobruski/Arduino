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
  Uma engine de narrativa ramificada interativa, construída para explorar consequências morais através de integração de hardware (Arduino), modelos de IA Generativa e uma interface gráfica fluida.
</p>

---

## 📌 Índice
* [Sobre o Projeto](#-sobre-o-projeto)
* [Arquitetura & Clean Code](#%EF%B8%8F-arquitetura--clean-code)
* [Interface e UX](#-interface-e-ux)
* [Como Executar](#-como-executar)
* [Integração Futura (Roadmap)](#-integração-futura-roadmap)

---

## 📖 Sobre o Projeto
Este sistema submete o usuário a cenários éticos complexos onde não há saída neutra — apenas decisões binárias de **SIM** ou **NÃO**. Projetado para demonstrar o fluxo de dados em tempo real entre um microcontrolador (atuando como sensor/gatilho) e uma aplicação Python local, alimentada por IA.

### ✨ Principais Funcionalidades
- **Árvore de Decisão Dinâmica:** Respostas moldam o próximo cenário instantaneamente.
- **Isolamento de Hardware:** Camada dedicada para leitura Serial assíncrona, evitando travamentos na interface.
- **IA Generativa (Plug & Play):** Arquitetura pronta para acoplar APIs de geração de texto (LLMs) para criar ramificações narrativas infinitas.

---

## ⚙️ Arquitetura & Clean Code
O projeto foi estruturado seguindo os princípios **SOLID** e **KISS**, separando estritamente a visão (View), o controle da lógica (Controller) e a integração externa (Hardware/AI).

<details>
<summary><b>📂 Clique para expandir a Estrutura de Diretórios</b></summary>
<br>

```text
projeto_arduino_python/
├── arduino/
│   └── firmware/
│       └── firmware.ino           # Código C/C++ da placa
├── python/
│   ├── src/
│   │   ├── hardware/              # Leitura/escrita da porta serial
│   │   ├── core/                  
│   │   │   └── ai_client.py       # Wrapper isolado para chamadas de API (IA)
│   │   ├── ui/                    
│   │   │   └── main_window.py     # Interface gráfica e folhas de estilo (QSS)
│   │   └── main.py                # Ponto de entrada, Threads e Orquestração
│   ├── tests/                     # Testes unitários
│   ├── config.json                # Configurações de ambiente (COM port, API keys)
│   └── requirements.txt           # Dependências (PyQt5)
└── README.md
