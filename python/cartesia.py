import requests
import string

ID_ROMARIO = "8047c415-af02-46fe-9bf8-7bc03348d61a"
ID_GAULES = "340d7ffe-aedf-450b-a6f4-a45d4badf11b"
ID_XUXA = "25a8c526-5bad-41dc-a265-2b15f4b7a74e"
ID_TRUMP = "7ef16b67-d341-4b17-8eb4-04b9e2cea953"

def converteTextoAudio(pessoa,texto):
    url = "https://api.cartesia.ai/tts/bytes"

    if pessoa == "Romario":
        idAtual = ID_ROMARIO
        nomeAudio = "romario.mp3"
    elif pessoa == "Gaules":
        idAtual = ID_GAULES
        nomeAudio = "gaules.mp3"
    elif pessoa == "Xuxa":
        idAtual = ID_XUXA
        nomeAudio = "xuxa.mp3"
    elif pessoa == "Trump":
        idAtual = ID_TRUMP
        nomeAudio = "trump.mp3"

    payload = {
        "model_id": "sonic-2",
        "transcript": texto,
        "voice": {
            "mode": "id",
            "id": idAtual
        },
        "output_format": {
            "container": "mp3",
            "bit_rate": 128000,
            "sample_rate": 44100
        },
        "language": "pt"
    }
    headers = {
        "Cartesia-Version": "2025-04-16",
        "Authorization": "Bearer sk_car_HsZziYnfjWFR6C9ENj77fr",
        "Content-Type": "application/json"
    }
    
    
    response = requests.post(url, json=payload, headers=headers)
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))

    if response.status_code == 200:
        with open(nomeAudio, "wb") as f:
            f.write(response.content)
        print("Áudio salvo como:", nomeAudio)
    else:
        print("Erro:", response.status_code, response.text)
        
    print("Texto enviado para Cartesia:", repr(texto))



# pessoa = "Gaules"
# texto = "Meu nome é gaules e gosto de jogar cs e meter muita bala"
# converteTextoAudio(pessoa,texto)





