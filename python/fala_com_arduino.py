from serial import Serial
from threading import Thread, Timer
from time import sleep
from cv2 import *
from traceback import format_exc

    
def ler_serial():
  while True:
    if meu_serial != None:
      texto_recebido = meu_serial.readline().decode().strip()
      if texto_recebido != "":
        print("recebido: " + texto_recebido)
        # ESCREVA AQUI O SEU CÓDIGO DA SERIAL!
        
        
        #print("[INFO] Arduino sinalizou que está pronto")
        #envia_serial("aberto")  # <- só envia aqui

    sleep(0.01)
    

# CASO A SERIAL NÃO FUNCIONE, COMENTE A LINHA ABAIXO E DESCOMENTE A SEGUINTE
meu_serial = Serial("COM7", baudrate=115200, timeout=0.1)
#meu_serial = None

print("[INFO] Serial conectada")

thread = Thread(target=ler_serial)
thread.daemon = True
thread.start()  


def envia_serial(coisa):

  # ESCREVA AQUI O CÓDIGO DO TIMER RECORRENTE
  # # # print("Enviando mensagem para arduino...")
  
  if meu_serial is not None:
      meu_serial.write((coisa+ "\n").encode())
