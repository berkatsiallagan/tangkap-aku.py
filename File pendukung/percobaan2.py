from tkinter import *

def klikTombol():
    label.configure(text="Tombol cek ditekan!")

def cekList():
    selected = listbox.selection_get()
    label.configure(text=selected)

root = Tk()
root.title("PROGRAM PERCOBAAN 2")

btn = Button(root, text="Cek", width=15, command=klikTombol)
btn.grid(column=0, row=1, pady=5)

data = { 1:".py", 2:".java", 3:".php"}
listbox = Listbox(root)
for k,v in data.items():
    listbox. insert(k,v)
listbox.grid(column=0, row=2, padx=10)

btn = Button(root, text="Cek List", width=15, command=cekList)
btn.grid(column=0, row=4, pady=5)

label = Label(root)
label.grid(column=0, row=5)

root.mainloop ()