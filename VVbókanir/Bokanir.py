import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

file_path = os.path.expanduser("~/Desktop/VVbókanir/bok.csv")

def lesa_skra(file=file_path):
    bok = []
    with open(file,mode="r",newline="") as skra:
        reader = csv.DictReader(skra)
        bok = list(reader)
    return bok

def skrifa_skra(nyBokun,file=file_path):
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

def BokunGUI(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="nafn").grid(row=0,column=0,padx=10, pady=10)
    tk.Label(main_frame, text="klukkan").grid(row=1,column=0,padx=10, pady=10)
    tk.Label(main_frame, text="dagsetning").grid(row=2,column=0,padx=10, pady=10)
    tk.Label(main_frame,text="bílnúmer").grid(row=3,column=0,padx=10, pady=10)

    name_entry = tk.Entry(main_frame,width=50)
    klukkan_entry = tk.Entry(main_frame,width=50)
    dagsetning_entry = tk.Entry(main_frame,width=50)
    bilnumer_entry = tk.Entry(main_frame,width=50)

    name_entry.grid(row=0,column=1,padx=10, pady=10)
    klukkan_entry.grid(row=1,column=1,padx=10, pady=10)
    dagsetning_entry.grid(row=2,column=1,padx=10, pady=10)
    bilnumer_entry.grid(row=3,column=1,padx=10, pady=10)

    def bokari():
        nafn = name_entry.get()
        klukkan = klukkan_entry.get()
        dagsetning = dagsetning_entry.get()
        bilnumer = bilnumer_entry.get()
        if not nafn.strip():
            messagebox.showwarning('vantar upplýsingar')
            return
        vistabok(nafn,klukkan,dagsetning,bilnumer)
    
    submit_button = tk.Button(main_frame,text="Bóka Tíma",command=bokari)
    submit_button.grid(row=4,column=0,columnspan=2,pady=10)

    skipta_button = tk.Button(main_frame,text="Skoða Bók",command=lambda:skoða_bok(main_frame))
    skipta_button.grid(row=5,column=0,columnspan=2,pady=10)


def skoða_bok(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    columns = ("nafn","klukkan","dagsetning","bílnúmer")
    tree = ttk.Treeview(main_frame,columns=columns,show="headings")

    for col in columns:
        tree.heading(col,text=col.capitalize())

    bokanir = lesa_skra()
    for idx, bok in enumerate(bokanir):
        tree.insert("",tk.END,iid=idx,values=(bok["nafn"],bok["klukkan"],bok["dagsetning"],bok["bílnúmer"]))
    
    tree.grid(row=0,column=0,columnspan=4,padx=10, pady=10,sticky="nsew")

    def eyða_bok():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Engin bókun var valin til að eyða")
            return
        selected_item = tree.selection()[0]
        tree.delete(selected_item)
        bokanir.pop(int(selected_item))
        skrifa_skra(bokanir)

    def breyta_bokun():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Engin bókun var valin til að breyta")
            return
        selected_item = tree.selection()[0]
        values = tree.item(selected_item,"values")
        breyta_bok_GUI(main_frame,values,selected_item,bokanir)

    delete_button = tk.Button(main_frame,text="Eyða Bókun",command=eyða_bok)
    delete_button.grid(row=1,column=0,padx=10, pady=10)

    edit_button = tk.Button(main_frame,text="breyta bókun",command=breyta_bokun)
    edit_button.grid(row=1,column=1,padx=10, pady=10)

    skipta_button = tk.Button(main_frame,text="Ný Bókun",command=lambda:BokunGUI(main_frame))
    skipta_button.grid(row=1,column=2,padx=10, pady=10)

def breyta_bok_GUI(main_frame,bok_values,item_id,bokanir):
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Nafn").grid(row=0,column=0,padx=10, pady=10)
    tk.Label(main_frame, text="Klukkan").grid(row=1,column=0,padx=10, pady=10)
    tk.Label(main_frame, text="Dagsetning").grid(row=2,column=0,padx=10, pady=10)
    tk.Label(main_frame, text="bílnúmer").grid(row=3,column=0,padx=10, pady=10)

    name_entry = tk.Entry(main_frame,width=50)
    name_entry.insert(0,bok_values[0])
    klukkan_entry = tk.Entry(main_frame,width=50)
    klukkan_entry.insert(0,bok_values[1])
    dagsetning_entry = tk.Entry(main_frame,width=50)
    dagsetning_entry.insert(0,bok_values[2])
    bilnumer_entry = tk.Entry(main_frame,width=50)
    bilnumer_entry.insert(0,bok_values[3])

    name_entry.grid(row=0,column=1,padx=10, pady=10)
    klukkan_entry.grid(row=1,column=1,padx=10, pady=10)
    dagsetning_entry.grid(row=2,column=1,padx=10, pady=10)
    bilnumer_entry.grid(row=3,column=1,padx=10, pady=10)


    def breytt_bokun():
        bokanir[int(item_id)] = {"nafn":name_entry.get(),"klukkan":klukkan_entry.get(),"dagsetning":dagsetning_entry.get(),"bílnúmer":bilnumer_entry.get()}
        skrifa_skra(bokanir)
        skoða_bok(main_frame)

    submit_button = tk.Button(main_frame,text="breyta",command=breytt_bokun)
    submit_button.grid(row=3,column=0,columnspan=2,pady=10)

    skipta_button = tk.Button(main_frame,text="hætta við",command=lambda:skoða_bok(main_frame))
    skipta_button.grid(row=4,column=0,columnspan=2,pady=10)

def main():
    root = tk.Tk()
    root.title("VV Bókunar Kerfi")
    root.geometry("600x400")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH,expand=True)
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    BokunGUI(main_frame)

    root.mainloop()

if __name__ == "__main__":
    main()
