from tkinter import *

def cekBilangan():
    bil = int(inputBil.get())
    if bil < 2:
        msg = f"{bil} bukan bilangan prima!"
    else:
        # Cek apakah bilangan prima
        is_prima = True
        for i in range(2, int(bil**0.5) + 1):
            if bil % i == 0:
                is_prima = False
                break
        if is_prima:
            msg = f"{bil} adalah bilangan prima!"
        else:
            msg = f"{bil} bukan bilangan prima!"
    lblMessage.configure(text=msg)

root = Tk()

root.title("PROGRAM CEK BILANGAN PRIMA")

# Label instruksi
lbl = Label(root, text="Input bilangan:")
lbl.grid(column=0, row=0, padx=10, pady=10)

# Input field
inputBil = Entry(root, width=25)
inputBil.grid(column=1, row=0, padx=10, pady=10)

# Tombol cek
btn = Button(root, text="Cek", width=15, command=cekBilangan)
btn.grid(column=0, row=1, pady=5, columnspan=2)

# Label untuk menampilkan hasil
lblMessage = Label(root, text="Masukkan bilangan untuk diperiksa.")
lblMessage.grid(column=0, row=2, columnspan=2, pady=10)

root.mainloop()
