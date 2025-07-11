# 🤖 Chatbot Interativo com Voz, Emoções e Arduino

Este projeto tem como objetivo a criação de uma cabeça de robô interativo que entende mensagens escritas ou por voz e responde com base na personalidade de personagens famosos usando IA (inteligência artificial). O robô também expressa emoções com a voz e com movimentos físicos usando Arduino e servomotores.

## 🧠 Objetivo

Criar uma interface inteligente que:
- Receba mensagens por **texto** ou **áudio**.
- Interprete a mensagem assumindo a **personalidade de um personagem** (Romário, Trump, Xuxa ou Gaules) com IA.
- Responda por **áudio sintetizado** com a voz do personagem.
- Detecte a **emoção** na resposta (felicidade, raiva, tristeza, confusão).
- Controle um robô físico com **servos** (via Arduino) para expressar emoções enquanto fala.

## 📦 Requisitos

- Python 3.x
- Bibliotecas:
  - `google-generativeai`
  - `SpeechRecognition`
  - `pyaudio`
  - `soundfile`
  - `Pillow`
- Arduino + servos
- Arquivo `.ino` carregado no Arduino para controlar movimentos via porta serial

## 🔧 Instalação

```bash
pip install -U google-generativeai
pip install SpeechRecognition pyaudio soundfile Pillow
```

> Certifique-se de que o Arduino está conectado à porta correta e que você tem permissão para acessar a porta serial.

## ⚙️ Componentes do Projeto

- `ia-gemini_emocoes_versao4.py`: Interface gráfica principal com botões e interação com o usuário.
- `gravador.py`: Responsável por gravar o áudio do microfone.
- `speech_to_text_audio.py`: Converte o áudio gravado para texto.
- `cartesia.py`: Converte o texto de resposta para áudio com a voz do personagem.
- `funcaoEnergia.py`: Analisa a energia do áudio para controlar a boca do robô.
- `fala_com_arduino.py`: Envia comandos para o Arduino via porta serial.

## 🤖 Robô Físico

- Feito com Arduino e 6 servomotores:
  - 2 servos controlam a **boca** (abertura sincronizada com a fala).
  - 4 servos controlam a **expressão facial** (ex: sobrancelha) com base na emoção detectada.
      - sendo 2 dos servos para os olhos (olhar para esquerda e direita)
      - e os outros 2 para as sobrancelhas
- Comandos são enviados em tempo real pela serial, como por exemplo:
  ```
  sobrancelha 2 0.7
  ```
