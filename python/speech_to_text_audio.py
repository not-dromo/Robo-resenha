import speech_recognition as sr

def speech_to_text(nomeAudio):

    # Inicializa o reconhecedor
    r = sr.Recognizer()

    # Carrega o áudio
    with sr.AudioFile(nomeAudio) as source:
        audio_data = r.record(source)

    # Google Web Speech API (grátis e fácil)
    try:
        text = r.recognize_google(audio_data, language='pt-BR')
        return text
    except Exception as e:
        print("Google Web Speech falhou:", e)


# #Arquivo de audio deve estar no mesmo diretório do script
# texto = speech_to_text("teste1.wav") #Nome do arquivo de audio 
# print(texto)
