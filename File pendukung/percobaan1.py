from tkinter import *

root = Tk()
root.geometry("800x600")
root.title("PROGRAM PERCOBAAN 1")

label = Label(root, text = "Ini adalah label")
label.grid(column=0, row=0)

input = Entry(root, width=50)
input.grid(column=1, row=1)

radio1 = Radiobutton(root, text="Nama Radio 1", value="valueRadio1", variable="grupradio")
radio1.grid(column=2, row=2)
radio1 = Radiobutton(root, text="Nama Radio 2", value="valueRadio2", variable="grupradio")
radio1.grid(column=3, row=2)

data = { 1:".py", 2:".java", 3:".php"}
listbox = Listbox(root)
for k,v in data.items():
    listbox.insert(k,v)
listbox.grid(column=0, row=3, padx=10)

btn = Button(root, text="Cek", width=15)
btn.grid(column=3, row=4, pady=25)

root.mainloop()