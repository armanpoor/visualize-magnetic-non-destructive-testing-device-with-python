from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import ( FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def get_file_name(file_entry):
    filename = fd.askopenfilename(title="Select file", filetypes=(("CSV Files", "*.csv"),))
    file_entry.delete(0, END)
    file_entry.insert(0, filename)

    import os
    base_name = os.path.basename(filename)
    Title = os.path.splitext(base_name)[0]
    print('FILE', Title)
    data = pd.read_csv(filename, encoding='utf-8', index_col=0).iloc[:, 2:22]
    df = data.unstack().reset_index()
    df.columns = ["X", "Y", "Z"]
    #df['X'] = pd.Categorical(df['X'])
    #df['X'] = df['X'].cat.codes
    df['X'] = pd.factorize(df['X'])[0] + 1

    tk_root = tk.Tk()

    figure = Figure(figsize=(12, 8))
    ax = figure.add_subplot(1, 1, 1, projection='3d')
    ax.plot_trisurf(df['X'], df['Y'], df['Z'], cmap=plt.cm.jet, linewidth=0.01, shade=True)
    ax.set_xlabel('Sensors')
    ax.set_ylabel('Shaft Encoder(cm)')
    ax.set_zlabel('value')
    canvas = FigureCanvasTkAgg(figure, tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.mpl_connect('button_press_event', ax._button_press)
    canvas.mpl_connect('button_release_event', ax._button_release)
    canvas.mpl_connect('motion_notify_event', ax._on_move)

def close(event=None):
    master.withdraw() # if you want to bring it back
    sys.exit() # if you want to exit the entire thing

master = Tk()
master.title("3d ploting by TKINTER")

entry_csv=Entry(master, text="", width=50)
entry_csv.grid(row=0, column=1, sticky=W, padx=5)

Label(master, text="Input CSV").grid(row=0, column=0 ,sticky=W)
Button(master, text="open&plot", width=10, command=lambda:get_file_name(entry_csv)).grid(row=0, column=2, sticky=W)

#Button(master, text="Plot", command=ploting, width=10).grid(row=3, column=1, sticky=E, padx=5)
Button(master, text="Cancel", command=close, width=10).grid(row=3, column=2, sticky=W)

#master.bind('<Return>', ploting)
master.bind('<Escape>', close)
mainloop()