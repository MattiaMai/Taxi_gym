import tkinter as tk
import numpy as np
from tkinter import ttk
from tkinter import *

numero_righe_taxi = 10
numero_colonne_taxi = 14

grid_rows = numero_righe_taxi
grid_columns = numero_colonne_taxi + (numero_colonne_taxi - 1)
# QUESTO PERCHE NELL'ENVIROMENT TAXI CI SONO CASELLE IN CUi IL TAXI NON CAMMINA E VANNO MESSI I MURI!


# grid_data = [[None] * grid_columns for _ in range(grid_rows)]
# Struttura dati per memorizzare i dati delle caselle
grid_data=np.full((grid_rows,grid_columns),None)
for row in range(grid_rows):
    for col in range(grid_columns):
        if ((col + 1) % 2 == 0):
            # INIZIALIZZO TUTTI GLI IPOTETICI MURI VERTICALI COME ASSENTI (:)
            grid_data[row][col] = ":"
        else:
            grid_data[row][col] = f"({row + 1},{int(col / 2) + 1})"  # python lavora per difetto

def add_line(row, column): #FUNZIONE PER INSERIRE IL VALORE NELLA GRIGLIA DEI DATI
    # line=entry.get()  # Ottieni il testo inserito nell'Entry
    line = tendina.get()  # Ottieni il testo inserito nel menu a tendina
    grid_data[row][column] = line  # Rimpiazza il valore della casella nella struttura dati


def button_clicked(event):#FUZIONE PER CAMBIARE IL TESTO DEL PULSANTE CON IL TESTO DELLA TENDINA UNA VOLTA PREMUTO
    button = event.widget
    button.configure(text=tendina.get())

def save_data(): #FUNZIONE CHE MI SALVA TUTTI I DATI PRESENTI NELLA GRIGLIE IN UN FILE dati.txt
    global data_string
    with open("dati.txt", "w") as fw:
        for row in range(0, grid_rows):
            for column in range(0, grid_columns):
                fw.write(f"{grid_data[row][column]} \n")

    print("Dati salvati correttamente.")


# Creazione della finestra principale
root = tk.Tk()

root.title("Editor mappa taxi")
# LE DIMENSIONI DELLA finestra SONO CIRCA: COLONNE* x (RIGHE*40)
dim = str(45 * grid_columns) + "x" + str(52 * grid_rows)
root.geometry(dim)

# Creazione della griglia
cell_width = 45
cell_height = 41
# SE SI CAMBIANO QUESTE DIMENSIONI CAMBAIRE ANCHE width e height a riga 73 e 75 per la grandezza dei pulsanti


# Creazione griglia di pulsanti
buttons = []
for row in range(grid_rows):
    for col in range(grid_columns):
        if ((col + 1) % 2 == 0):
            button = tk.Button(root, text=f":", width=5, height=2, command=lambda r=row, c=col: add_line(r, c), bg="red")
            button.grid(row=row, column=col)
            button.bind("<Button-1>", button_clicked)
            buttons.append(button)
            # INIZIALIZZO TUTTI GLI IPOTETICI MURI VERTICALI COME ASSENTI (:)
            #cell = tk.Button(root, text=f":", width=5, height=2, command=lambda r=row, c=col: add_line(r, c), bg="red")
        else:
            button = tk.Button(root, text=f"({row + 1},{int(col / 2) + 1})", width=5, height=2,command=lambda r=row, c=col: add_line(r, c))
            button.grid(row=row, column=col)
            button.bind("<Button-1>", button_clicked)
            buttons.append(button)


# Pulsante per salvare i dati
save_button = tk.Button(root, text="Salva", command=save_data)
#save_button.pack(side="bottom")
#METODI GEOMETRY (come grid) E PACK NON POSSONO ESSERE USATI INSIEME
save_button.grid(row=grid_rows+1, columnspan=grid_columns)


"""
# Creazione dell'Entry per l'inserimento del testo
entry = tk.Entry(root, width=8)
entry.configure(justify="center")
entry.pack(side="bottom")
"""

# CREAZIONE MENU A TENDINA PER SCELTA DI OSTACOLO
ostacolo = StringVar()
tendina = ttk.Combobox(root, textvariable=ostacolo, width=16)
tendina['values'] = ["Inserisci ostacolo", "-", "|", ":", " "]
tendina.current(0)
def remove_default_option(event):
    # Rimuovi l'opzione predefinita dalla lista di valori
    tendina['values'] = ["-", "|", ":", " "]

tendina.bind("<<ComboboxSelected>>", remove_default_option)  # Rimuovi l'opzione predefinita dopo la selezione

tendina['state'] = 'readonly'
tendina.configure(justify="center")
#tendina.pack(side='bottom')
tendina.grid(row=grid_rows+2, columnspan=grid_columns)


# Avvio dell'applicazione
root.mainloop()

# ora ho dati.txt , voglio creare una mappa come taxy
# TRADUTTORE DA MAPPA A TESTO PER TAXI

pu_elem = "+" + grid_columns * "-" + "+"  # Primo e Ultimo ELEMENTO di MAP
MAP = ["" for i in range(grid_rows + 2)]
MAP[grid_rows + 1] = pu_elem
MAP[0] = pu_elem

fr = open("dati.txt", "r")

for i in range(1, grid_rows + 1):
    stringa = ""
    for j in range(grid_columns + 2):
        if (j == 0):
            stringa = stringa + "|"
        elif (j == grid_columns + 1):
            stringa = stringa + "|"
        else:
            c = fr.readline()
            if (c == "- \n"):
                stringa = stringa + "-"
            elif (c == "| \n"):
                stringa = stringa + "|"
            elif (c == ": \n"):
                stringa = stringa + ":"
            else:
                stringa = stringa + " "

    MAP[i] = stringa

# SCRITTURA DELLA MAPPA
fw = open("MAPPA.txt", "w")
fw.write("MAP=[\n")
for i in range(grid_rows + 2):
    if i == grid_rows + 1:
        fw.write("\"" + str(MAP[i]) + "\"\n")  # se è l'ultimo elemento non metto la virgola finale
    else:
        fw.write("\"" + str(MAP[i]) + "\",\n")
fw.write("]")
fw.close()

fr.close()

