from tkinter import *

def cekBilangan():
    bil = int(inputBil.get())
    if bil%2 == 0:
        msg = f"{bil} adalah bilangan genap!"
    else:
        msg = f"{bil} adalah bilangan ganjil!"
    lblMessage.configure(text=msg)

root = Tk()

root. title("PROGRAM GENAP-GANJIL")

lbl = Label(root, text = "Input bilangan :")
lbl.grid(column=0, row=0)

inputBil = Entry(root, width=25)
inputBil.grid(column=1, row=0)

btn = Button(root, text="Cek", width=15, command=cekBilangan)
btn.grid(column=0, row=1, pady=5)

lblMessage = Label(root)
lblMessage.grid(column=0, row=2)

root.mainloop ()