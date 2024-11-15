import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


def temperature_distribution(X, Y, W, H, T1, Tm, terms):

    T = np.zeros_like(X) + T1  # Initialise la température avec T1
    for n in range(1, terms + 1, 2):  # On prend seulement les termes impairs
        Cn = (4 * Tm) / (np.pi * n)
        T += Cn * np.sin(n * np.pi * X / W) * np.sinh(n * np.pi * Y / W) / np.sinh(n * np.pi * H / W)
    return T


def plot_temperature():
    """
    Fonction pour tracer la distribution de température et les lignes de courant dans la plaque rectangulaire.
    """
    T1 = float(entry_T1.get())
    Tm = float(entry_Tm.get())
    W = float(entry_W.get())
    H = float(entry_H.get())
    terms = int(entry_terms.get())

    # Crée la grille pour le calcul
    x = np.linspace(0, W, 100)
    y = np.linspace(0, H, 50)
    X, Y = np.meshgrid(x, y)

    T = temperature_distribution(X, Y, W, H, T1, Tm, terms)

    fig.clear()
    ax = fig.add_subplot(111)

    contour = ax.contourf(X, Y, T, levels=20, cmap='coolwarm')
    fig.colorbar(contour, ax=ax, label="Température (°C)")
    ax.contour(X, Y, T, colors='black', linewidths=0.5, linestyles='solid')

    Tx, Ty = np.gradient(-T)

    ax.streamplot(X, Y, Tx, Ty, color='black', linewidth=0.5)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Isothermes et lignes de courants ")

    canvas.draw()


root = tk.Tk()
root.title("Simulation de Température")

frame = ttk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

ttk.Label(frame, text="Température T1 (°C):").grid(row=0, column=0)
entry_T1 = ttk.Entry(frame)
entry_T1.insert(0, "20")  # Valeur par défaut
entry_T1.grid(row=0, column=1)

ttk.Label(frame, text="Amplitude Tm (°C):").grid(row=1, column=0)
entry_Tm = ttk.Entry(frame)
entry_Tm.insert(0, "80")  # Valeur par défaut
entry_Tm.grid(row=1, column=1)

ttk.Label(frame, text="Largeur W:").grid(row=2, column=0)
entry_W = ttk.Entry(frame)
entry_W.insert(0, "10")  # Valeur par défaut
entry_W.grid(row=2, column=1)

ttk.Label(frame, text="Hauteur H:").grid(row=3, column=0)
entry_H = ttk.Entry(frame)
entry_H.insert(0, "5")  # Valeur par défaut
entry_H.grid(row=3, column=1)

ttk.Label(frame, text="Nombre de termes:").grid(row=4, column=0)
entry_terms = ttk.Entry(frame)
entry_terms.insert(0, "50")  # Valeur par défaut
entry_terms.grid(row=4, column=1)

update_button = ttk.Button(frame, text="Mettre à jour", command=plot_temperature)
update_button.grid(row=5, columnspan=2, pady=10)

fig = plt.Figure(figsize=(6, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

plot_temperature()

root.mainloop()
