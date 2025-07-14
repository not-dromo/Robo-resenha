# 🤖 Chatbot Interativo com Voz, Emoções e Arduino

Este projeto tem como objetivo a criação de uma cabeça de robô interativo que entende mensagens escritas ou por voz e responde com base na personalidade de personagens famosos usando IA (inteligência artificial). O robô também expressa emoções com a voz e com movimentos físicos usando Arduino e servomotores.

## 🧠 Funcionamento

- Interface gráfica desenvolvida com **Tkinter**.
- Botões para selecionar o personagem que responderá: **Romário, Trump, Xuxa ou Gaules**.
- Após a escolha do personagem:
  - O usuário grava um áudio usando o microfone.
  - O áudio é transcrito para texto com a **API Whisper do Google**.
  - O texto é enviado para a **API Gemini**, que gera uma resposta baseada na personalidade escolhida.
  - O texto da resposta é convertido em áudio com a **API da Cartesia**, com base no personagem escolhido.
  - A resposta é analisada para identificar a **emoção predominante**:  
    - Felicidade  
    - Raiva  
    - Tristeza  
    - Confusão
  - Durante a reprodução do áudio, a boca do robô se movimenta através de dois servos, de acordo com a **energia do som**, simulando a fala.
  - A emoção é enviado via **serial para o Arduino**, que controla os **servomotores** responsáveis pela sombrancelha e olhos:

### Tecnologias e APIs utilizadas:

- Python + Tkinter (interface gráfica)
- Google Whisper (transcrição de áudio)
- Google Gemini (geração de resposta com base na personalidade)
- Cartesia (conversão de texto em áudio)
- Arduino + Servomotores (expressões faciais robóticas)

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
- `arduino-teste.ino`: controle dos servos do rosto robótico

## 🤖 Robô Físico

- Feito com Arduino e 6 servomotores:
  - 2 servos controlam a **boca** (abertura sincronizada com a fala).
  - 4 servos controlam a **expressão facial** (ex: sobrancelha) com base na emoção detectada.
      - sendo 2 dos servos para os olhos (olhar para esquerda e direita)
      - e os outros 2 para as sobrancelhas


<img width="2748" height="1488" alt="image" src="https://github.com/user-attachments/assets/2a2a4343-fdfa-477e-b6fe-1b7c25025efb" />
