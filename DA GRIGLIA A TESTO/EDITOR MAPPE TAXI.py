import tkinter as tk
import numpy as np
from tkinter import ttk
from tkinter import *

numero_righe_taxi=10
numero_colonne_taxi=14


grid_rows = numero_righe_taxi
grid_columns = numero_colonne_taxi+(numero_colonne_taxi-1)
#QUESTO PERCHE NELL'ENVIROMENT TAXI CI SONO CASELLE IN CUi IL TAXI NON CAMMINA E VANNO MESSI I MURI!

#grid_data = [[None] * grid_columns for _ in range(grid_rows)]
# Struttura dati per memorizzare i dati delle caselle
grid_data=np.full((grid_rows,grid_columns),None)
for row in range(grid_rows):
    for col in range(grid_columns):
        if ((col + 1) % 2 == 0):
            # INIZIALIZZO TUTTI GLI IPOTETICI MURI VERTICALI COME ASSENTI (:)
            grid_data[row][col] = ":"
        else:
            grid_data[row][col] = f"({row + 1},{int(col/2) + 1})"#python lavora per difetto

def add_line(row, column):
    #line=entry.get()  # Ottieni il testo inserito nell'Entry
    line=tendina.get() #Ottieni il testo inserito nel menu a tendina
    grid_data[row][column] = line  # Rimpiazza il valore della casella nella struttura dati
    draw_grid()  # Ridisegna la griglia con i dati aggiornati


def save_data():
    global data_string
    with open("dati.txt", "w") as fw:
        for row in range(0, grid_rows):
            for column in range(0, grid_columns):
                fw.write(f"{grid_data[row][column]} \n")

    print("Dati salvati correttamente.")


def draw_grid():
    canvas.delete("all")  # Cancella il contenuto precedente del canvas
    for row in range(grid_rows):
        for col in range(grid_columns):
            cell_data = grid_data[row][col]
            if cell_data is not None:
                #quisti +0.5 servono per centrale la scrittura, canvas
                #è come una tela, la struttura a griglia l'ho data io
                canvas.create_text((col + 0.5) * cell_width, (row + 0.5) * cell_height,text=cell_data)  # Posiziona il testo al centro della cella

            canvas.create_rectangle(col * cell_width, row * cell_height, (col + 1) * cell_width,(row + 1) * cell_height)


# Creazione della finestra principale
root = tk.Tk()

root.title("Editor mappa taxi")
#LE DIMENSIONI DELLA finestra SONO CIRCA: COLONNE* x (RIGHE*40)
dim=str(45*grid_columns)+"x"+str(70*grid_rows)
root.geometry(dim)

# Creazione della griglia
cell_width = 45
cell_height = 32
#SE SI CAMBIANO QUESTE DIMENSIONI CAMBAIRE ANCHE width e height a riga 73 e 75 per la grandezza dei pulsanti

canvas = tk.Canvas(root, width=grid_columns * cell_width, height=grid_rows * cell_height)
canvas.pack(side="bottom")

#Creazione griglia di pulsanti
for row in range(grid_rows):
    for col in range(grid_columns):
        if((col+1)%2==0):
            #INIZIALIZZO TUTTI GLI IPOTETICI MURI VERTICALI COME ASSENTI (:)
            cell = tk.Button(root,text=f":", width=5, height=1, command=lambda r=row, c=col: add_line(r, c), bg="red")
        else:
            cell = tk.Button(root,text=f"({row + 1},{int(col/2) + 1})", width=5, height=1, command=lambda r=row, c=col: add_line(r, c))

        cell.place(x=col * cell_width, y=row * cell_height)


#INIZIALIZZAZIONE DELLA TELA (in modo che compaia la posizione)
for row in range(grid_rows):
    for col in range(grid_columns):
        if ((col + 1) % 2 == 0):
            canvas.create_text((col + 0.5) * cell_width, (row + 0.5) * cell_height,text=":")  # Posiziona il testo al centro della cella
            canvas.create_rectangle(col * cell_width, row * cell_height, (col + 1) * cell_width,(row + 1) * cell_height)
        else:
            canvas.create_text((col + 0.5) * cell_width, (row + 0.5) * cell_height,text=f"({row + 1},{int(col/2) + 1})")  # Posiziona il testo al centro della cella
            canvas.create_rectangle(col * cell_width, row * cell_height, (col + 1) * cell_width, (row + 1) * cell_height)


# Pulsante per salvare i dati
save_button = tk.Button(root, text="Salva", command=save_data)
save_button.pack(side="bottom")

"""
# Creazione dell'Entry per l'inserimento del testo
entry = tk.Entry(root, width=8)
entry.configure(justify="center")
entry.pack(side="bottom")
"""

#CREAZIONE MENU A TENDINA PER SCELTA DI OSTACOLO
ostacolo=StringVar()
tendina=ttk.Combobox(root,textvariable=ostacolo,width=16)
tendina['values']= ["Inserisci ostacolo", "-", "|", ":", " "]
tendina.current(0)
def remove_default_option(event):
    # Rimuovi l'opzione predefinita dalla lista di valori
        tendina['values'] = ["-", "|", ":", " "]

tendina.bind("<<ComboboxSelected>>", remove_default_option)  # Rimuovi l'opzione predefinita dopo la selezione

tendina['state']='readonly'
tendina.configure(justify="center")
tendina.pack(side='bottom')



# Avvio dell'applicazione
root.mainloop()


#ora ho dati.txt , voglio creare una mappa come taxy
#TRADUTTORE DA MAPPA A TESTO PER TAXI

pu_elem = "+"+ grid_columns*"-"+"+" #Primo e Ultimo ELEMENTO di MAP
MAP = ["" for i in range(grid_rows+2)]
MAP[grid_rows+1]=pu_elem
MAP[0]=pu_elem

fr=open("dati.txt","r")

for i in range(1,grid_rows+1):
    stringa = ""
    for j in range(grid_columns+2):
        if(j==0):
            stringa=stringa+"|"
        elif (j==grid_columns+1):
            stringa = stringa + "|"
        else:
            c = fr.readline()
            if (c=="- \n") :
                stringa=stringa+"-"
            elif (c=="| \n"):
                stringa=stringa+"|"
            elif (c==": \n"):
                stringa=stringa+":"
            else:
                stringa=stringa+" "

    MAP[i]=stringa


#SCRITTURA DELLA MAPPA
fw=open("MAPPA.txt","w")
fw.write("MAP=[\n")
for i in range(grid_rows+2):
    if i==grid_rows+1:
        fw.write("\""+str(MAP[i])+"\"\n")#se è l'ultimo elemento non metto la virgola finale
    else:
        fw.write("\"" + str(MAP[i]) + "\",\n")
fw.write("]")
fw.close()


fr.close()

'''
RISULTATO SE USO LA MAPPA VUOTA
['+---------+', 
 '| : : : : |', 
 '| : : : : |', 
 '| : : : : |', 
 '| : : : : |', 
 '| : : : : |', 
 '+---------+']
 
 ESEMPIO CON MAPPA FATTA DA ME
 MAP=['+---------+', 
  '| | --:-: |',
  '| | | : |-|',
  '| : | : |-|',
  '| | : | : |',
  '| | : | : |',
  '+---------+']

 
'''
