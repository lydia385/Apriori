import tkinter as tk
import Ap
from tkinter import filedialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 

root = tk.Tk()
root.geometry("800x600")
root.title("Apriori")
df = None
def open_file_dialog():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    if file_path:
        df = pd.read_csv(file_path)
        
        text.delete('1.0', tk.END)
        for column in df.columns:
            text.insert(tk.END, column)
            text.insert(tk.END, "\n")
        text.insert(tk.END, "\n")
        text.insert(tk.END, "Data shape: ")
        text.insert(tk.END, (df.shape))
        text.insert(tk.END, "\nValue count: \n\n")
        text.insert(tk.END, df.value_counts())


       


def display_data():
    global canvas
    if canvas is not None:
         
       clear_canvas()
    global df

    if df is not None:
        text.delete('1.0', tk.END)
        text.insert(tk.END, str(df))
        

canvas = None
def Visualization():
    global df
    global canvas

    fig = Figure(figsize=(7, 4))
    ax = fig.add_subplot(111)
    ax.hist(df)
    ax.set_title("Frequncy of each instance")
    plt.xlabel("instance")
    plt.ylabel("Frequency")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=1)
def clear_canvas():
        global canvas
        canvas.get_tk_widget().grid_forget()



label = tk.Label(root, text="MinSup")
entry = tk.Entry(root)
def AprioriFun():
    global canvas
    global df
    if df is None:
         text.insert(tk.END, "\n please import data")
    try:
        number = float(entry.get())
        if number is not None:
            if number <=0 :
                print('jdsh')
                text.insert(tk.END, "\n minsup can't be <= 0")
            else:
                dk,F_iteamset = Ap.apriori(df,number)
                rules = Ap.generate_association_rules(dk, 0.9,metric='confidence')

    except ValueError:
         m=Ap.autominsup(df)
         print("hnnhh",type(m),m)
         dk,F_iteamset = Ap.apriori(df,m)
         rules = Ap.generate_association_rules(dk, 0.9,metric='confidence')
    
    if canvas is not None:
       clear_canvas()
    
    
    text.delete('1.0', tk.END)
    for i in range(rules.shape[0]):
        text.insert(tk.END, str(rules.iloc[i,0]))
        text.insert(tk.END, " ==> ")
        text.insert(tk.END, str(rules.iloc[i,1]))  
        text.insert(tk.END, "\n")
        text.insert(tk.END, "<confidence> ")
        text.insert(tk.END,str(rules.iloc[i,3][0]))  
        text.insert(tk.END, "     <Lift> ")

        text.insert(tk.END,str(rules.iloc[i,4][0]))  
        text.insert(tk.END, "\n\n")

def CloseFun():
    global canvas
    global df
    if canvas is not None:
       clear_canvas()
    F_iteamset = Ap.close(df,0.15)
    text.delete('1.0', tk.END)
    for i in range(F_iteamset):
        text.insert(tk.END, str(i[i]))
       





OpenFile = tk.Button(root, text="Open File", width=15, height=1, bd=4, relief="ridge",fg = "Blue",command=open_file_dialog)
OpenFile.grid(row=0, column=0,padx=5, pady=5)

display = tk.Button(root, text="Display Data", width=15, height=1, bd=4, relief="ridge",fg = "Blue",command=display_data)
display.grid(row=1, column=0,padx=5, pady=5)

Visualizer = tk.Button(root, text="Visualization", width=15, height=1, bd=4, relief="ridge",fg = "Blue",command=Visualization)
Visualizer.grid(row=2, column=0)

Apriori = tk.Button(root, text="Apriori", width=15, height=1, bd=4, relief="ridge",fg = "Blue",command=AprioriFun)
Apriori.grid(row=0, column=1,padx=5, pady=5)



text = tk.Text(root)
text.grid(row=3, column=1)
label.grid(row=1, column=1)
entry.grid(row=2, column=1)




# Démarrer la boucle principale de l'interface graphique
root.mainloop()