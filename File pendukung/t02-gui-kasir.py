from tkinter import *
from tkinter import messagebox

# Fungsi untuk menghitung total harga setelah diskon
def hitungTotal():
    try:
        harga = int(inpHarga.get())
        jumlah = int(inpJumlah.get())
        member = grupMember.get()

        # Daftar diskon berdasarkan jenis member
        diskon_dict = {
            "None": 0,
            "Silver": 10,
            "Gold": 25,
            "Platinum": 50,
            "Diamond": 75
        }

        # Mendapatkan persentase diskon
        jenis_member = [key for key, val in diskon_dict.items() if val == int(member)][0]
        diskon = diskon_dict[jenis_member]

        # Hitung total harga
        total_harga = harga * jumlah
        harga_diskon = total_harga - (total_harga * diskon / 100)

        # Tampilkan hasil
        messagebox.showinfo("Total Harga", f"Member: {jenis_member}\nTotal Harga: Rp{total_harga:,}\nHarga Setelah Diskon: Rp{harga_diskon:,}")
    except ValueError:
        messagebox.showerror("Input Error", "Pastikan semua input diisi dengan angka yang valid.")

root = Tk()
root.title("PROGRAM KASIR SEDERHANA")
root.geometry("600x400")

# Input harga barang
lblHarga = Label(root, text="Input harga barang:")
lblHarga.grid(column=0, row=0, padx=10, pady=5)
inpHarga = Entry(root, width=25)
inpHarga.grid(column=1, row=0, padx=10, pady=5)

# Input jumlah barang
lblJumlah = Label(root, text="Input jumlah barang:")
lblJumlah.grid(column=0, row=1, padx=10, pady=5)
inpJumlah = Entry(root, width=25)
inpJumlah.grid(column=1, row=1, padx=10, pady=5)

# Pilihan jenis member
lblMember = Label(root, text="Pilih jenis member:")
lblMember.grid(column=0, row=2, pady=5)
grupMember = StringVar()
grupMember.set(0)  # Default pilihan

# Daftar member dan diskon
members = {"None": 0, "Silver": 10, "Gold": 25, "Platinum": 50, "Diamond": 75}
rowRadio = 3
for key, val in members.items():
    Radiobutton(root, text=key, variable=grupMember, value=val).grid(column=1, row=rowRadio, sticky=W, padx=10)
    rowRadio += 1

# Tombol untuk menghitung total harga
btn = Button(root, text="Hitung Total", background="green", foreground="white", width=20, command=hitungTotal)
btn.grid(column=0, row=rowRadio, columnspan=2, pady=10)

root.mainloop()
