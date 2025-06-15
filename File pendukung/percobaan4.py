from tkinter import *
from tkinter import messagebox

def cekTotal():
    harga = int(inpHarga.get())
    member = grupMember.get()
    messagebox.showinfo("Data Form", f"Member: {member}, harga: {harga}")

root = Tk()
root.title("PROGRAM KASIR SEDERHANA")
root.geometry("600x400")

lblHarga = Label(root, text = "Input harga barang :")
lblHarga.grid(column=0, row=0)
inpHarga = Entry(root, width=25)
inpHarga.grid(column=1, row=0)

# Buat dictionary untuk daftar jenis member
members = { "None":0, "Silver":1, "Gold":2, "Platinum":3, "Diamond":4 }

lblMember = Label(root, text = "Pilih jenis member:")
lblMember.grid(column=0, row=2, pady=5)
grupMember = StringVar()
rowRadio = 2
for key,val in members.items():
    Radiobutton(root, text=key, variable=grupMember, value=val, ).grid(column=1, row=rowRadio, sticky=W)
rowRadio+=1
grupMember.set(0)

btn = Button(root, text="Hitung", background="green", foreground="white", width=15, command=cekTotal)
btn.grid(column=0, pady=5)

root.mainloop()