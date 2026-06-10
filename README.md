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
* [Hardware — Arduino](#-hardware--arduino)
* [Como Executar](#-como-executar)
* [Gerar Executável (.exe)](#-gerar-executável-exe)
* [Roadmap](#-roadmap)

---

## 📖 Sobre o Projeto
Este sistema apresenta ao usuário cenários éticos complexos onde não há saída neutra — apenas decisões binárias de **SIM** ou **NÃO**. Foi projetado para demonstrar o fluxo de dados em tempo real entre um microcontrolador (sensor/gatilho) e uma aplicação Python local, alimentada por IA generativa.

### ✨ Principais Funcionalidades
- **Árvore de decisão dinâmica:** respostas moldam o próximo cenário em tempo real.
- **Controle via hardware:** as escolhas SIM/NÃO vêm exclusivamente dos botões físicos do Arduino — sem interação por mouse ou teclado.
- **Interface imersiva:** fundo pixel-art animado de lua sobre a água com estrelas piscando, ondulações e reflexos em movimento.
- **Isolamento de hardware:** leitura serial assíncrona em thread separada, evitando travamentos na UI.
- **IA generativa (plug & play):** arquitetura pronta para conectar qualquer LLM via `core/ai_client.py`.

---

## ⚙️ Arquitetura & Clean Code
O projeto segue separação de responsabilidades — View, Controller, Hardware e IA completamente isolados.

<details>
<summary><b>📂 Estrutura de Diretórios</b></summary>
<br>

```text
Arduino/
├── core/
│   ├── ai_client.py       ← integração com a API de IA (plug & play)
│   └── data_parser.py     ← interpreta mensagens do Arduino
├── hardware/
│   └── serial_client.py   ← leitura serial assíncrona (QThread)
├── ui/
│   └── main_window.py     ← interface gráfica com fundo pixel-art animado
├── Placa/
│   └── codigoplaca.c      ← firmware do Arduino
├── config.json            ← porta serial e baud rate
├── requirements.txt
├── build.bat              ← script para gerar o .exe
├── README.md
└── main.py                ← controlador principal
```
</details>

---

## 🎨 Interface e UX
- **Fundo pixel-art** gerado em Python puro via `QPainter`: céu noturno, lua com sombreamento esférico e crateras, reflexo ondulado na água.
- **Animações a 24 FPS** via `QTimer`: estrelas piscando individualmente, ondulações percorrendo a água, brilho pulsante no reflexo lunar e reflexos cintilantes (glitter).
- **Painel translúcido** sobreposto ao fundo com texto em `#F2EDD5` (creme quente) — contraste superior ao WCAG AAA.
- **Sem botões na UI** — toda interação vem da placa Arduino.

---

## 🔌 Hardware — Arduino

### Componentes
| Componente | Pino | Função |
|---|---|---|
| Botão 1 | 2 | Escolha **SIM** |
| LED Verde | 8 | Feedback visual do botão 1 |
| Botão 2 | 5 | Escolha **NÃO** |
| LED Vermelho | 11 | Feedback visual do botão 2 |

### Protocolo Serial
| Evento | Mensagem enviada | Python interpreta |
|---|---|---|
| Boot da placa | `ARDUINO_READY` | Exibe "Arduino conectado e pronto" na UI |
| Botão 1 pressionado | `BUTTON1:HIGH` | `SIM` → gera consequência na IA |
| Botão 2 pressionado | `BUTTON2:HIGH` | `NÃO` → gera consequência na IA |

> Os LEDs acendem enquanto o botão está pressionado e apagam ao soltar.

---

## 🚀 Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Ajuste a porta serial em `config.json` (padrão: `COM3`):
   ```json
   { "serial_port": "COM3", "baud_rate": 9600, "timeout": 1.0 }
   ```
3. Carregue o firmware `Placa/codigoplaca.c` no Arduino via Arduino IDE.
4. Conecte o Arduino via USB e execute:
   ```bash
   python main.py
   ```

> Se o Arduino não estiver conectado, o programa inicia normalmente e exibe o erro serial na UI — a IA ainda funciona.

---

## 📦 Gerar Executável (.exe)

Para distribuir sem precisar de Python instalado, execute na pasta do projeto:

```
build.bat
```

O script verifica se as dependências já estão instaladas (pula o pip na segunda vez), compila e gera:

```
dist/
├── DilemasEticos.exe
└── config.json        ← edite aqui para trocar a porta COM
```

> Para trocar a porta serial após compilado, basta editar `dist/config.json` — não precisa recompilar.

---

## 📌 Roadmap
- Conectar API de IA em `core/ai_client.py` (Gemini, OpenAI, Claude, etc.)
- Reconexão automática da serial em caso de desconexão do Arduino
- Suporte a múltiplos idiomas nos cenários éticos
- Testes unitários para o parser serial e a lógica de controle
