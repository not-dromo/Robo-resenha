import numpy as np
import soundfile as sf
import sounddevice as sd
import os
from fala_com_arduino import envia_serial

def calcularEnergia(nomeArquivo):
    if not os.path.exists(nomeArquivo):
        print(f"Arquivo não encontrado: {nomeArquivo}")
        return

    # Lê o áudio
    vetorAmostras, taxaAmostragem = sf.read(nomeArquivo)
    vetorAmostras = np.atleast_2d(vetorAmostras).T  # garante (N, canais)

    # Parâmetros
    tamanhoJanelaTempo = 50  # ms
    amostrasPorJanela = int(taxaAmostragem * tamanhoJanelaTempo / 1000)

    # Divide em janelas e calcula energia
    energias = []
    for i in range(0, len(vetorAmostras), amostrasPorJanela):
        janela = vetorAmostras[i:i + amostrasPorJanela]
        if len(janela) == 0:
            continue
        energia = np.sum(janela ** 2)
        energias.append(energia)

    # Normaliza
    energias = np.array(energias)
    energias = (energias - np.min(energias)) / (np.max(energias) - np.min(energias))

    # Variável de estado
    estado = {'pos': 0, 'janela_index': 0}

    def audio_callback(outdata, frames, time_info, status):
        if status:
            print(status)

        pos = estado['pos']
        fim = pos + frames

        # Preenche os frames de saída
        out = vetorAmostras[pos:fim]
        if len(out) < frames:
            out = np.pad(out, ((0, frames - len(out)), (0, 0)))

        outdata[:] = out
        estado['pos'] = fim

        # Mostra energia sincronizada por tempo real
        janela_index = estado['janela_index']
        if janela_index < len(energias):
            # print(f"Tempo: {janela_index * tamanhoJanelaTempo / 1000:.2f}s | Energia: {energias[janela_index]:.3f}")
            envia_serial(f"voz {energias[janela_index]:.3f}")
            estado['janela_index'] += 1

    # Inicia reprodução com callback
    # print("\n[ÁUDIO] Iniciando reprodução com callback sincronizado")
    with sd.OutputStream(
        samplerate=taxaAmostragem,
        channels=vetorAmostras.shape[1],
        callback=audio_callback,
        blocksize=amostrasPorJanela
    ):
        sd.sleep(int(len(vetorAmostras) / taxaAmostragem * 1000)) # Mantem o programa em esperar enquanto o audio ta sendo executado para que o script nao acabe enquanto o audio ainta ta sendo reproduzido

    print("\n[FIM] Reprodução finalizada.")

# Chamada da função
if __name__ == "__main__":
    calcularEnergia("romario.mp3")
