# Python para o Radiuino over Arduino
import serial
import math
import time
import struct
import socket
from time import localtime, strftime
import os

def calc_rssi(byte):
   rssi =0
   if byte > 128:
      rssi = ((byte-256)/2.0)-74
   else:
      rssi = (byte/2.0)-74
   return rssi

# Configura a serial
# para COM# o número que se coloca é n-1 no primeiro parâmetrso. Ex COM9  valor 8
n_serial = input("Digite o número da serial = ") #seta a serial
n_serial1 = int(n_serial) - 1
ser = serial.Serial("COM"+str(n_serial), 9600, timeout=0.5,parity=serial.PARITY_NONE) # serial Windows
#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # serial Linux

#apaga o arquivo de medidas
if os.path.exists("RSSI_B_1.txt"): # esse arquivo é apagado a cada rodada
   os.remove("RSSI_B_1.txt")

if os.path.exists("RSSI_1_2.txt"): # esse arquivo é apagado a cada rodada
   os.remove("RSSI_1_2.txt")

filename1 = strftime("LOG_RSSI_B_1_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename2 = "RSSI_B_1.txt" # esse arquivo será apagado a cada nova rodada de medidas
filename3 = strftime("LOG_RSSI_1_2_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename4 = "RSSI_1_2.txt" # esse arquivo será apagado a cada nova rodada de medidas

print ("Arquivo de log: %s" % filename1)
Log_dados_B_1 = open(filename1, 'w')
Log_dados_1_2 = open(filename3, 'w')

# Salva títulos das colunas no arquivo de log
print ('Time stamp;Contador;RSSI_B_1;RSSI_1_B',file=Log_dados_B_1)
print ('Time stamp;Contador;RSSI_1_2;RSSI_2_1',file=Log_dados_1_2)

# Entra com quantas medidas vai realizar
#num_medidas = input('Entre com o número de medidas = ')
num_medidas = 1000000

# Cria o vetor Pacote
Pacote_TX =[0]*52
Pacote_RX=[0]*52

# Cria Pacote de 52 bytes com valor zero em todas as posições
for i in range(52): # faz um array com 52 bytes
   Pacote_TX[i] = 0
   Pacote_RX[i] = 0

#inicializa variáveis auxiliares
w = int(num_medidas)+1
perda_PK_RX =0
i = 0
contador = 0
PKT_down = 0

try:
   # ============ Camada Física - Transmite o pacote        
   for j in range(1,w):
   
      # ==== Camada de Transporte contagem de pacotes de descida
      PKT_down = PKT_down + 1
      if PKT_down == 256:
         PKT_down = 0
      Pacote_TX[12] = PKT_down

   # ============= Camada de Aplicação comandos para a placa

      arquivo = open('ROTA.txt', 'r') # leitura do arquivo comandos_oficina.txt que estão nas linhas
      Pacote_TX[8] = int(arquivo.readline())
      Pacote_TX[9] = int(arquivo.readline())
      Pacote_TX[10] = int(arquivo.readline())
      Pacote_TX[11] = int(arquivo.readline())
      Pacote_TX[16] = int(arquivo.readline())
      Pacote_TX[17] = int(arquivo.readline())
      Pacote_TX[18] = int(arquivo.readline())
      Pacote_TX[19] = int(arquivo.readline())
      Pacote_TX[20] = int(arquivo.readline())      
      arquivo.close()

## ============= CAMDA FÍSICA TRANSMITE O PACOTE            

# nenhuma informação
                  
      for k in range(52): # transmite pacote
         TXbyte = chr(Pacote_TX[k])
         ser.write(TXbyte.encode('latin1'))
               
      # Aguarda a resposta do sensor
      time.sleep(0.5)
      
   # ============= Camada Física - Recebe o pacote
      Pacote_RX = ser.read(52) # faz a leitura de 52 bytes do buffer que rec

      if len(Pacote_RX) == 52:
         # RSSI byte 21 - RX NO NÓ 1 VINDO DA BASE
         RSSI_B_1 = calc_rssi(Pacote_RX[19])
        
         # RSSI byte 28 - RX NO         
         RSSI_1_B = calc_rssi(Pacote_RX[22])
      
         # RSSI byte 22 - RX NO         
         RSSI_1_2 = calc_rssi(Pacote_RX[20])

         # RSSI byte 27 - RX N        
         RSSI_2_1 = calc_rssi(Pacote_RX[21])


         PKTup = Pacote_RX[14] * 256 + Pacote_RX[15]

   # ============= Camada Aplicação
         print ('Cont=',j,'| B-1=',RSSI_B_1,'| 1-B=',RSSI_1_B,'| 1-2 =',RSSI_1_2,'| 2-1 =',RSSI_2_1)

         # Salva no arquivo de log
         print (time.asctime(),';',j,';',RSSI_B_1,';',RSSI_1_B,file=Log_dados_B_1)
         Medidas_rssi_B_1 = open(filename2, 'a+')
         print (j,';',RSSI_B_1,';',RSSI_1_B,file=Medidas_rssi_B_1)
         Medidas_rssi_B_1.close()
         
         print (time.asctime(),';',j,';',RSSI_1_2,';',RSSI_2_1,file=Log_dados_1_2)
         Medidas_rssi_1_2 = open(filename4, 'a+')
         print (j,';',RSSI_1_2,';',RSSI_2_1,file=Medidas_rssi_1_2)
         Medidas_rssi_1_2.close()
         
      else: #Caso de erro de recepção
         perda_PK_RX = perda_PK_RX+1
         print ('Cont = ', j,' PERDEU PACOTE ')
         
         # Salva no arquivo de log
         print (time.asctime(),';',j,';;',file=Log_dados_B_1)
         Medidas_B_1 = open(filename2, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_B_1)
         Medidas_B_1.close()

         print (time.asctime(),';',j,';;',file=Log_dados_1_2)
         Medidas_1_2 = open(filename2, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_1_2)
         Medidas_1_2.close()

   print ('Pacotes enviados = ',j,' Pacotes perdidos = ',perda_PK_RX)
   Log_dados_B_1.close()
   Log_dados_1_2.close()   
   Medidas_B_1.close()
   Medidas_1_2.close()   
   ser.close()
   print ('Fim da Execução')  # escreve na tela

except KeyboardInterrupt:
   ser.close()
   Log_dados_B_1.close()
   Log_dados_1_2.close()   
   Medidas_B_1.close()
   Medidas_1_2.close()   

