import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os



def lesa_skra(file="bok.csv"):
    bok = []
    with open(file,mode="r",newline="") as skra:
        reader = csv.DictReader(skra)
        bok = list(reader)
    return bok

def skrifa_skra(nyBokun,file="bok.csv"):
    with open(file,mode="w",newline="") as skra:
        fieldnames = ["nafn","klukkan","dagsetning","bílnúmer"]
        writer = csv.DictWriter(skra,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(nyBokun)


def vistabok(nafn,klukkan,dagsetning,bilnr):
    bokun = lesa_skra()
    bokun.append({"nafn":nafn,"klukkan":klukkan,"dagsetning":dagsetning,"bílnúmer":bilnr})
    skrifa_skra(bokun)
    messagebox.showinfo("Nýbókun hefur verið skráð")

def BokunGUI():
    root = tk.Tk()
    root.title("Ný Bókun")

    tk.Label(root, text="nafn").grid(row=0,column=0)
    tk.Label(root, text="klukkan").grid(row=1,column=0)
    tk.Label(root, text="dagsetning").grid(row=2,column=0)
    tk.Label(root,text="bílnúmer").grid(row=3,column=0)

    name_entry = tk.Entry(root)
    klukkan_entry = tk.Entry(root)
    dagsetning_entry = tk.Entry(root)
    bilnumer_entry = tk.Entry(root)

    name_entry.grid(row=0,column=1)
    klukkan_entry.grid(row=1,column=1)
    dagsetning_entry.grid(row=2,column=1)
    bilnumer_entry.grid(row=3,column=1)

    def bokari():
        nafn = name_entry.get()
        klukkan = klukkan_entry.get()
        dagsetning = dagsetning_entry.get()
        bilnumer = bilnumer_entry.get()
        vistabok(nafn,klukkan,dagsetning,bilnumer)
    
    submit_button = tk.Button(root,text="Bóka Tíma",command=bokari)
    submit_button.grid(row=4,column=0,columnspan=2)

    root.mainloop()
BokunGUI()

def skoða_bok():
    root = tk.Tk()
    root.title("Bókanir")
    columns = ("nafn","klukkan","dagsetning","bílnúmer")
    tree = ttk.Treeview(root,columns=columns,show="headings")

    for col in columns:
        tree.heading(col,text=col.capitalize())

    bokanir = lesa_skra()
    for bok in enumerate(bokanir):
        tree.insert("",tk.END,values=(bok["nafn"],bok["klukkan"],bok["dagsetning"],bok["bílnúmer"]))
    
    tree.grid(row=0,column=0,columnspan=4)

    def eyða_bok():
        selected_item = tree.selection()[0]
        tree.delete(selected_item)
        bokanir.pop(int(selected_item))
        skrifa_skra(bokanir)

    def breyta_bokun():
        selected_item = tree.selection()[0]
        values = tree.item(selected_item,"values")
        breyta_bok_GUI(values,selected_item,bokanir)

    delete_button = tk.Button(root,text="Eyða Bókun",command=eyða_bok)
    delete_button.grid(row=1,column=0)

    edit_button = tk.Button(root,text="breyta bókun",command=breyta_bokun)
    edit_button.grid(row=1,column=1)

    root.mainloop()

def breyta_bok_GUI(bok_values,item_id,bokanir):
    edit_window = tk.Toplevel()
    edit_window.title("Breyta Bókun")

    tk.Label(edit_window, text="Nafn").grid(row=0,column=0)
    tk.Label(edit_window, text="Klukkan").grid(row=1,column=0)
    tk.Label(edit_window, text="Dagsetning").grid(row=2,column=0)
    tk.Label(edit_window, text="bílnúmer").grid(row=3,column=0)

    name_entry = tk.Entry(edit_window)
    name_entry.insert(0,bok_values[0])
    klukkan_entry = tk.Entry(edit_window)
    klukkan_entry.insert(0,bok_values[1])
    dagsetning_entry = tk.Entry(edit_window)
    dagsetning_entry.insert(0,bok_values[2])
    bilnumer_entry = tk.Entry(edit_window)
    bilnumer_entry.insert(0,bok_values[3])

    name_entry.grid(row=0,column=1)
    klukkan_entry.grid(row=1,column=1)
    dagsetning_entry.grid(row=2,column=1)
    bilnumer_entry.grid(row=3,column=1)


    def breytt_bokun():
        bokanir[int(item_id)] = {"nafn":name_entry.get(),"klukkan":klukkan_entry.get(),"dagsetning":dagsetning_entry.get(),"bílnúmer":bilnumer_entry.get()}
        skrifa_skra(bokanir)
        edit_window.destroy()
        skoða_bok()

    submit_button = tk.Button(edit_window,text="breyta",command=breytt_bokun)
    submit_button.grid(row=3,column=0,columnspan=2)

    edit_window.mainloop()

skoða_bok()

