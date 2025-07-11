import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# se tiver mais de um mic no pc use este comando para checar qual mic é o seu

# print(sd.query_devices())

# depois escreva o index dele na variável device_index

# Parâmetros
fs = 44100  # Frequência de amostragem (Hz)
duration = 5  # Duração da gravação (segundos)
device_index = 1

gravacao = []

stream = None

# def gravando():
#     print("Gravando...")
#     audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16', device = device_index)
#     sd.wait()
#     print("Gravação finalizada!")

#     # Salvar no arquivo WAV
#     write("teste1.wav", fs, audio)
#     print("Arquivo 'gravacao.wav' salvo!")

def inicia_gravacao():
    global gravacao, stream

    gravacao = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        gravacao.append(indata.copy())
    
    print("Gravando...")

    stream = sd.InputStream(samplerate = fs, channels = 1, dtype = "int16",
                           callback = callback, device = device_index)
    
    stream.start()

def para_gravacao():
    global gravacao, stream

    if stream:
        stream.stop()
        stream.close()

        print("Gravação finalizada!")

        audio_array = np.concatenate(gravacao, axis = 0)
        write("teste1.wav", fs, audio_array)
        print("Arquivo teste1.wav salvo!")
    else:
        print("Nenhuma gravação em andamento.")
        
        
if __name__ == "__main__":
    print(sd.query_devices())