import serial
import math
import time
import struct
from time import localtime, strftime
import schedule
import time
from tkinter import *
import tkinter.scrolledtext as ScrolledText

#from ScrolledText import ScrolledText
import threading
import matplotlib.pyplot as plt
#import ttk


#from Tkinter import *
#from ttk import *
import tkinter.ttk as ttk
#from tkFileDialog import asksaveasfilename
import tkinter.filedialog
#import tkMessageBox
import tkinter.messagebox as tkMessageBox
#from ScrolledText import ScrolledText

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure

from math import pow

import serial  # pyserial
import numpy as np
import serial.tools.list_ports
import pandas as pd

#import serial
import math
import time
#import struct
from time import localtime, strftime
import schedule
import time
#from Tkinter import *
#import tkMessageBox
#from ScrolledText import ScrolledText
import threading
import matplotlib.pyplot as plt
#import ttk
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,    NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
from tkinter.filedialog import asksaveasfilename
from datetime import datetime

style.use("ggplot")

#funcao que gera os graficos usando a matplotlib
        
def grafico(f,c):
        global s1

        f.clear()
    
        x = []
        y = []
        z= []
        psr=[]
        dados = open("RSSI_B_1.txt",'r')
        for line in dados:
            line=line.strip()
            #print (line)
            Y = line.split(';')
            y.append(Y)


        for i in range(len(y)):
            if((y[i][1])!='')and((y[i][2])!=''):
                x.append(float(y[i][1]))
                psr.append(float(y[i][2]))  # testando com 1
                z.append(float(y[i][0]))
             
        axis = f.add_subplot(211)
        axis.plot(z,x,label='RSSI B-1')
        axis.legend()
        axis.set_ylabel('dBm')

        axis1 = f.add_subplot(212)
        axis1.plot(z,psr,label='RSSI 1-B')
        axis1.legend()
        axis1.set_ylabel('dBm')
        f.subplots_adjust(left=0.12, bottom=0.09, right=0.98, top=0.95, wspace=None, hspace=None)
       
        c.draw()

        dados.close()
        raiz.after(1000, grafico,f,c)


def callback():
    if tkMessageBox.askokcancel("Sair", "Tem certeza que deseja sair?"):
        raiz.destroy()

def salvar(ff):
        ftypes = [('.png (PNG)', '*.png')]
        f = asksaveasfilename(filetypes=ftypes, defaultextension=".png")

        print(f)

        if f != '':
            ff.savefig(f)

#####----------------------------------------CRIAÇAO DA JANELA PRINCIPAL E FRAMES---------------------

raiz=Tk() #criando a tela principal , usando um objeto TKinter
raiz.title("RSSI SALTO B-1") #funcao para alterar titulo da janela
raiz.geometry('900x400') #define o tamanho da janela
raiz.resizable(0, 0) #deixa o tamanho da janela fixo, sem opções de redimensionamento

#frame_cima = Frame(master=raiz,borderwidth=1, relief='sunken') #cria um frame no topo da janela, define como master a janela principal(raiz)
#frame_meio = Frame(master=raiz,borderwidth=1, relief='sunken') #cria um frame no meio da janela, define como master a janela principal(raiz) 
frame_baixo = Frame(master=raiz,borderwidth=1, relief='sunken') #cria um frame no rodapé da janela, define como master a janela principal(raiz)

#frame_cima.place(x=10,y=10,width=980,height=100) #posiciona e define o tamanho dos frames
#frame_meio.place(x=10,y=120,width=980,height=210) #posiciona e define o tamanho dos frames
frame_baixo.place(x=10,y=10,width=980,height=580) #posiciona e define o tamanho dos frames

fig = Figure(figsize=(8.8, 4), facecolor='white')
b=Button(frame_baixo, text='Salvar Gráfico', command=lambda:salvar(fig))
b.place(x=460,y=530)
canvas = FigureCanvasTkAgg(fig, master=frame_baixo)
canvas.get_tk_widget().grid(row=3, column=1, columnspan=3, sticky='NSEW')
grafico(fig,canvas)       

###---------------------- CÓDIGO PARA RODAR A APLICAÇÃO

raiz.protocol("WM_DELETE_WINDOW", callback)
raiz.mainloop()









