import csv
from tkinter import filedialog, messagebox

def salvar_csv(dados):
    if not dados:
        messagebox.showwarning("Aviso", "Nenhuma simulação realizada ainda.")
        return

    arquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if arquivo:
        with open(arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ano", "Núcleos Restantes"])
            writer.writerows(dados)
        messagebox.showinfo("CSV Salvo", f"Arquivo salvo com sucesso: {arquivo}")

def salvar_grafico(fig):
    arquivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if arquivo:
        fig.savefig(arquivo)
        messagebox.showinfo("Salvo", f"Gráfico salvo como {arquivo}")
