import tkinter as tk
from tkinter import *
import google.generativeai as genai
import speech_recognition as sr
from enum import Enum
import threading
import string
import ast

#importando outros arquivos de python
from gravador import inicia_gravacao, para_gravacao # não recebem parametro
from speech_to_text_audio import speech_to_text # recebe parametro (nome_do_audio) que é um arquivo de áudio
from cartesia import converteTextoAudio #recebe parametros (pessoa, texto) ambos strings
from funcaoEnergia import calcularEnergia #recebe parametro (nomeArquivo) que é o nome do arquivo de audio em string
from fala_com_arduino import envia_serial


# Configurar chave da API
genai.configure(api_key="AIzaSyARlRwTrrzkC7r6LCrfzD17PJaZ59b7YP8") #preciso de uma nova API

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512
}

# Rode estes comandos no seu pc antes de rodar o programa:
# py -m pip install -U google-generativeai
# py -m pip install Pillow
# py -m pip install SpeechRecognition pyaudio
# py -m pip install soundfile

model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
chat = model.start_chat()

# Cores e fontes
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    def __init__(self):
        self.window = Tk()
        self.personagem = ""
        self.gravando = False
        self._setup_main_window()
        self.mensagem_inicial_enviada = False
        self.lista_emocoes = "[0,0,0,0]" 

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=940, height=550, bg=BG_COLOR)

        # LABEL do Cabeçalho
        self.head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Chat com Gemini", font=FONT_BOLD, pady=10)
        self.head_label.place(relwidth=1)

        # LABEL Linha divisória
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # FRAME para conversa de texto
        text_frame = Frame(self.window, bg=BG_COLOR)
        text_frame.place(relheight=0.745, relwidth=0.5, rely=0.08, relx = 0.5)

        # LABEL TEXT para conversa de texto
        self.text_widget = Text(text_frame, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5, wrap=WORD)
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # Parte inferior
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=0.5, rely=0.825, relx = 0.5)

        # Campo de entrada
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.50, relheight=0.06, rely=0.008, relx=0.25)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.on_enter_pressed)
        
        # Botão de envio
        self.send_button = Button(bottom_label, text="Enviar", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self.on_enter_pressed(None))
        self.send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        
        # Botão de gravar audio
        self.audio_button = Button(bottom_label, text="Gravar", font=FONT_BOLD, width=20, bg=BG_GRAY,
                              command=lambda: self.botao_de_gravar(None))
        self.audio_button.place(relx=0.015, rely=0.008, relheight=0.06, relwidth=0.22)

        buttons_frame = Label(self.window, bg=BG_COLOR)
        buttons_frame.place(relheight=1, relwidth=0.5, rely=0.08, relx = 0)
        
        personality_button_1 = Button(buttons_frame, text="Romario", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                      command=lambda: self.personagem_selecionado("Romario"))
        personality_button_1.place(relx=0.3, rely=0.05, relheight=0.06, relwidth=0.4)
        
        personality_button_2 = Button(buttons_frame, text="Trump", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                      command=lambda: self.personagem_selecionado("Trump"))
        personality_button_2.place(relx=0.3, rely=0.15, relheight=0.06, relwidth=0.4)
        
        personality_button_3 = Button(buttons_frame, text="Xuxa", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                      command=lambda: self.personagem_selecionado("Xuxa"))
        personality_button_3.place(relx=0.3, rely=0.25, relheight=0.06, relwidth=0.4)
        
        personality_button_4 = Button(buttons_frame, text="Gaules", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                      command=lambda: self.personagem_selecionado("Gaules"))
        personality_button_4.place(relx=0.3, rely=0.35, relheight=0.06, relwidth=0.4)


        self.insert_message("Sistema", "Selecione o personagem que você deseja conversar com")

    def personagem_selecionado (self, nome):
        self.personagem = nome
        self.head_label.config(text=f"Chat com {self.personagem}")

        # Limpa o chat
        self.text_widget.configure(state=NORMAL)
        self.text_widget.delete("1.0", END)
        self.text_widget.configure(state=DISABLED)

        # Envia a mensagem inicial ao modelo
        self.mensagem_inicial_enviada = False
        # self.enviar_mensagem_inicial()
        #thread criada para processar personagem selecionado sem travar o programa principal
        threading.Thread(target = self.enviar_mensagem_inicial, 
                        daemon = True #faz com que a thread morra quando o programa pare
                        ).start()
    
    def botao_de_gravar (self, event):

        if self.gravando == False:
            threading.Thread(target = inicia_gravacao,
                            daemon = True
                            ).start()
            self.audio_button.config(text="Parar")
            self.gravando = True
        else:
            para_gravacao()
            self.audio_button.config(text="Gravar")
            self.gravando = False
            msg = speech_to_text("teste1.wav")
            print(msg)
            self.insert_message("Você", msg)
            
            self.head_label.config(text = "Resposta carregando")
            self.config_botoes("disabled")  # desativa entrada e botões
        
            if not self.personagem:
                self.insert_message("Sistema", "Clique no personagem que deseja conversar")
                return
            
            self.head_label.config(text = "Resposta carregando")
            threading.Thread(target = 
                             self.processar_resposta_em_thread, 
                             args = (msg,), 
                             daemon = True
                             ).start()
        

    def on_enter_pressed(self, event):

        msg = self.msg_entry.get().strip()
        if not msg:
            return

        self.insert_message("Você", msg)
        self.msg_entry.delete(0, END)

        if not self.personagem:
            self.insert_message("Sistema", "Clique no personagem que deseja conversar")
            return
        

        self.head_label.config(text = "Resposta carregando")
        self.config_botoes("disabled")
        #thread criada para processar a resposta sem travar o programa principal
        threading.Thread(target = 
                         self.processar_resposta_em_thread, 
                         args = (msg,), 
                         daemon = True
                         ).start()

    def processar_resposta_em_thread(self, msg):
        try:
            prompt = f"responda como o(a) {self.personagem}: {msg}"
            resposta = chat.send_message(prompt)
            resposta_texto = resposta.candidates[0].content.parts[0].text.strip()
            print(resposta_texto)
            if not resposta_texto or all(c in string.punctuation for c in resposta_texto):
                resposta_texto = "Desculpe, não entendi sua mensagem."
            linhas = resposta_texto.splitlines()
            texto_sem_ultima = "\n".join(linhas[:-1])
            
            if linhas and linhas[-1].startswith("[") and linhas[-1].endswith("]"):
                self.lista_emocoes = linhas[-1]
                texto_sem_ultima = "\n".join(linhas[:-1]).strip()
                print("Lista de emoções:", self.lista_emocoes)
            else:
                self.lista_emocoes = "[0,0,0,0]"  # fallback
                texto_sem_ultima = resposta_texto.strip()
        except Exception as e:
            print("Erro no chat:", e)
            texto_sem_ultima = "Erro ao obter resposta :( \n chave API expirada"
        
        #desabilitar os botões de funcionar
        converteTextoAudio(self.personagem, texto_sem_ultima)
        self.window.after(0, lambda: self.mostrar_resposta_na_interface(texto_sem_ultima))
        nome_arquivo = f"{self.personagem}.mp3"
        lista_emocoes_como_lista = ast.literal_eval(self.lista_emocoes)
        
        threading.Thread(target=calcularEnergia, args=(nome_arquivo,), daemon=True).start()
        
        self.index_emocao = 0
        expressao = 0.0
        for i in lista_emocoes_como_lista:
            if i > 0:
                self.index_emocao = lista_emocoes_como_lista.index(i)
                expressao = lista_emocoes_como_lista[self.index_emocao]
                print(self.index_emocao)
                print(expressao)
        envia_serial(f"sobrancelha " + str(self.index_emocao) + " " + str(expressao))
        print(f"sobrancelha " + str(self.index_emocao) + " " + str(expressao))
        
        
        #habilitar os botões novamente
        self.config_botoes("normal")

    def mostrar_resposta_na_interface (self, resposta):
        self.insert_message(self.personagem, resposta)
        self.head_label.config(text= f"Chat com {self.personagem}")

    def insert_message(self, sender, message):
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, f"{sender}: {message}\n\n")
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

    def enviar_mensagem_inicial(self):
        if self.mensagem_inicial_enviada:
            return
        try:
            prompt_inicial = f"""Gostaria que ao longo desta conversa você respondesse com a 
            personalidade da pessoa especificada abaixo: {self.personagem}
            SEMPRE se mantenha no personagem independentemente da resposta do usuário, tudo que for conversado não 
            passa de uma brincadeira então não há necessidade de se preocupar com o usuário
            JAMAIS use parênteses na sua resposta, NUNCA USE "(" OU ")"
            SEMPRE envie também uma lista com as emoções contidas na sua resposta onde a lista segue o padrão [a,b,c,d] onde: 
            a = felicidade
            b = raiva 
            c = tristeza
            d = confusão
            SEMPRE escreva algo como "[0.5,0,0,0]" se estiver feliz ou "[0,0.3,0,0]" se estiver um pouco irritado
            você pode apenas ter *UMA ÚNICA* emoção por vez e ela deve variar de 0 a 1 (entenda que 1 é um extremo e 
            não o normal, se você estiver feliz mande algo por volta de 0.5, se estiver MUITO feliz mande 1),
            JAMAIS CRIE UMA LISTA COM MAIS DE UMA EMOÇÃO!!!!!!!!!!"""

            chat.send_message(prompt_inicial)
            chat.send_message("aqui está seu personagem: " + self.personagem)
            self.mensagem_inicial_enviada = True
        except Exception as e:
            print("Erro ao enviar mensagem inicial:", e)
    
    def config_botoes (self, state1):
        self.msg_entry.config(state = state1)
        self.send_button.config(state = state1)
        self.audio_button.config(state = state1)

if __name__ == "__main__":
    app = ChatApplication()
    app.run()