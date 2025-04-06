import tkinter as tk
from tkinter import messagebox, filedialog
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv


def simular_decaimento_radioativo(qtd_inicial: int, taxa: float, anos: int) -> tuple[list[int], list[int]]:
    quantidade_nucleos = [qtd_inicial]
    anos_passados = [0]
    nucleos_restantes = qtd_inicial
    log = [f"Ano 0: {qtd_inicial} núcleos restantes"]

    for ano in range(1, anos + 1):
        sobreviventes = sum(1 for _ in range(nucleos_restantes) if random.random() > taxa)
        nucleos_restantes = sobreviventes
        anos_passados.append(ano)
        quantidade_nucleos.append(nucleos_restantes)
        log.append(f"Ano {ano}: {nucleos_restantes} núcleos restantes")

    return anos_passados, quantidade_nucleos, log


def exibir_grafico(tempos: list[int], quantidades: list[int]) -> None:
    global fig, canvas
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(tempos, quantidades, marker='o', color='#5A189A')

    for x, y in zip(tempos, quantidades):
        ax.annotate(f"({x},{y})", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)

    ax.set_title('Simulação de Decaimento Radioativo')
    ax.set_xlabel('Tempo (anos)')
    ax.set_ylabel('Número de Núcleos Atômicos')
    ax.grid(True)
    canvas.draw()


def iniciar_simulacao() -> None:
    try:
        qtd_inicial = int(entry_qtd.get())
        taxa_decaimento = float(entry_taxa.get())
        duracao = int(entry_anos.get())

        if not (0 < taxa_decaimento < 1):
            raise ValueError("A taxa de decaimento deve estar entre 0 e 1.")

        tempos, quantidades, log = simular_decaimento_radioativo(qtd_inicial, taxa_decaimento, duracao)
        exibir_grafico(tempos, quantidades)
        atualizar_logs(log)

        global ultimos_dados_csv
        ultimos_dados_csv = list(zip(tempos, quantidades))

    except ValueError as e:
        messagebox.showerror("Erro de entrada", str(e))


def atualizar_logs(logs: list[str]) -> None:
    text_logs.config(state='normal')
    text_logs.delete(1.0, tk.END)
    for linha in logs:
        text_logs.insert(tk.END, linha + "\n")
    text_logs.config(state='disabled')


def salvar_grafico() -> None:
    arquivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if arquivo:
        fig.savefig(arquivo)
        messagebox.showinfo("Salvo", f"Gráfico salvo como {arquivo}")


def salvar_csv() -> None:
    if not ultimos_dados_csv:
        messagebox.showwarning("Aviso", "Nenhuma simulação realizada ainda.")
        return

    arquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if arquivo:
        with open(arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ano", "Núcleos Restantes"])
            writer.writerows(ultimos_dados_csv)
        messagebox.showinfo("CSV Salvo", f"Arquivo salvo com sucesso: {arquivo}")


ultimos_dados_csv = []

janela = tk.Tk()
janela.title("Simulador de Decaimento Radioativo")
janela.configure(padx=20, pady=20)

# Frame de entrada
frame_inputs = tk.Frame(janela)
frame_inputs.grid(row=0, column=0, sticky="nw")

tk.Label(frame_inputs, text="Quantidade Inicial de Átomos:").grid(row=0, column=0, sticky="w")
entry_qtd = tk.Entry(frame_inputs, width=25)
entry_qtd.grid(row=0, column=1, pady=5)

tk.Label(frame_inputs, text="Taxa de Decaimento (0 a 1):").grid(row=1, column=0, sticky="w")
entry_taxa = tk.Entry(frame_inputs, width=25)
entry_taxa.grid(row=1, column=1, pady=5)

tk.Label(frame_inputs, text="Duração (em anos):").grid(row=2, column=0, sticky="w")
entry_anos = tk.Entry(frame_inputs, width=25)
entry_anos.grid(row=2, column=1, pady=5)

botao_simular = tk.Button(frame_inputs, text="Simular", width=20, bg="#5A189A", fg="white", command=iniciar_simulacao)
botao_simular.grid(row=3, column=0, columnspan=2, pady=10)

botao_salvar = tk.Button(frame_inputs, text="Salvar Gráfico", width=20, command=salvar_grafico)
botao_salvar.grid(row=4, column=0, columnspan=2, pady=5)

botao_csv = tk.Button(frame_inputs, text="Salvar CSV", width=20, command=salvar_csv)
botao_csv.grid(row=5, column=0, columnspan=2, pady=5)

# Frame para gráfico e logs
frame_visual = tk.Frame(janela)
frame_visual.grid(row=0, column=1, padx=20)

# Gráfico
fig = plt.figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_visual)
canvas.get_tk_widget().pack()

# Logs
text_logs = tk.Text(frame_visual, height=10, width=50, state='disabled', bg="#F5F5F5")
text_logs.pack(pady=10)

janela.mainloop()
