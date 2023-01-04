# WissTek-two-hops (Dois saltos)

## Sobre

- Elemento de borda: Raspberry pi 3 + BE9x0 (alias B).
- 2 Nós sensores: BE9x0 (Alias 1 e 2).

Elemento de borda se conecta com os sensores, rota possuí seguinte trajeto: B -> 1, 1 -> 2, 2 -> 1 e enfim 1 -> B.



## Comunicação serial - Raspberry com BE9x0

Para podemos utilizar a serial, precisamos primeiro importar as funções da serial. Para mais informações consulte: [import](https://docs.python.org/3/reference/import.html)

```python
import serial
```

Depois de adicionar todas as importações ao código, definição de funções, podemos então começar a escrever as linhas de código que configuram a porta serial. Quando rodamos esse código utilizando SO Windows, devemos comentar a linha que configura serial em sistema Linux. Lembrando que em python, para comentar uma linha de código utilizamos o símbolo cerquilha '#'.
```python
ser = serial.Serial("COM"+str(n_serial), 9600, timeout=0.5,parity=serial.PARITY_NONE) # serial Windows
#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # serial Linux
```
Quando rodamos o código em Linux, comentamos a linha que configura serial para Windows.
```python
#ser = serial.Serial("COM"+str(n_serial), 9600, timeout=0.5,parity=serial.PARITY_NONE) # serial Windows
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # serial Linux

```
Código final da serial:
```python
# Configura a serial
# para COM# o número que se coloca é n-1 no primeiro parâmetrso. Ex COM9  valor 8
n_serial = input("Digite o número da serial = ") #seta a serial
n_serial1 = int(n_serial) - 1
ser = serial.Serial("COM"+str(n_serial), 9600, timeout=0.5,parity=serial.PARITY_NONE) # serial Windows
#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # serial Linux
```
Vamos falar agora sobre>

```python
def calc_rssi(byte):
   rssi =0
   if byte > 128:
      rssi = ((byte-256)/2.0)-74
   else:
      rssi = (byte/2.0)-74
   return rssi
```
