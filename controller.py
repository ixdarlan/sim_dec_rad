import csv
import os
from tkinter import filedialog
import matplotlib.pyplot as plt

def salvar_csv(dados):
    if not dados:
        return

    caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not caminho:
        return

    with open(caminho, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["Ano", "Núcleos Restantes"])
        for ano, qtd in dados:
            writer.writerow([ano, qtd])

def salvar_grafico(figura):
    caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if not caminho:
        return
    figura.savefig(caminho)

def salvar_csv_personalizado(tempos, quantidades, caminho):
    with open(caminho, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["Ano", "Núcleos Restantes"])
        for ano, qtd in zip(tempos, quantidades):
            writer.writerow([ano, qtd])

def salvar_grafico_personalizado(tempos, quantidades, caminho):
    fig, ax = plt.subplots()
    ax.plot(tempos, quantidades, marker='o', color='#5A189A')
    ax.set_title('Simulação de Decaimento Radioativo')
    ax.set_xlabel('Tempo (anos)')
    ax.set_ylabel('Número de Núcleos Atômicos')
    ax.grid(True)

    for x, y in zip(tempos, quantidades):
        ax.annotate(f"({x},{y})", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)

    fig.tight_layout()
    fig.savefig(caminho)
    plt.close(fig)
