import tkinter as tk
from tkinter import messagebox, filedialog
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def mostrar_logo_console():
    logo = """
   ____  _                 _       _             
  / ___|| |__   __ _ _ __ | | ___ (_)_ __   __ _ 
  \___ \| '_ \ / _` | '_ \| |/ _ \| | '_ \ / _` |
   ___) | | | | (_| | |_) | | (_) | | | | | (_| |
  |____/|_| |_|\__,_| .__/|_|\___/|_|_| |_|\__, |
                    |_|                   |___/ 
    """
    print(logo)
    print("Simulador de Decaimento Radioativo Iniciado\n")


def simular_decaimento_radioativo(qtd_inicial: int, taxa: float, anos: int) -> tuple[list[int], list[int]]:
    print(f"Quantidade Inicial: {qtd_inicial}")
    print(f"Taxa de Decaimento: {taxa}")
    print(f"Duração: {anos} anos\n")

    quantidade_nucleos = [qtd_inicial]
    anos_passados = [0]
    nucleos_restantes = qtd_inicial

    for ano in range(1, anos + 1):
        sobreviventes = sum(1 for _ in range(nucleos_restantes) if random.random() > taxa)
        nucleos_restantes = sobreviventes
        anos_passados.append(ano)
        quantidade_nucleos.append(nucleos_restantes)
        print(f"Ano {ano}: {nucleos_restantes} núcleos restantes")

    print("\nSimulação concluída.\n")
    return anos_passados, quantidade_nucleos


def exibir_grafico(tempos: list[int], quantidades: list[int]) -> None:
    global fig, canvas
    fig.clear()

    ax = fig.add_subplot(111)
    ax.plot(tempos, quantidades, marker='o', color='purple')

    for x, y in zip(tempos, quantidades):
        ax.annotate(f"({x},{y})", (x, y), textcoords="offset points", xytext=(5, 5), ha='left', fontsize=8)

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

        tempos, quantidades = simular_decaimento_radioativo(qtd_inicial, taxa_decaimento, duracao)
        exibir_grafico(tempos, quantidades)

    except ValueError as e:
        messagebox.showerror("Erro de entrada", str(e))


def salvar_grafico() -> None:
    arquivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if arquivo:
        fig.savefig(arquivo)
        messagebox.showinfo("Salvo", f"Gráfico salvo como {arquivo}")
        print(f"Gráfico salvo em: {arquivo}")


mostrar_logo_console()

janela = tk.Tk()
janela.title("Simulador de Decaimento Radioativo")

tk.Label(janela, text="Quantidade Inicial de Átomos:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_qtd = tk.Entry(janela)
entry_qtd.grid(row=0, column=1, padx=10, pady=5)

tk.Label(janela, text="Taxa de Decaimento (0 a 1):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_taxa = tk.Entry(janela)
entry_taxa.grid(row=1, column=1, padx=10, pady=5)

tk.Label(janela, text="Duração (em anos):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_anos = tk.Entry(janela)
entry_anos.grid(row=2, column=1, padx=10, pady=5)

botao_simular = tk.Button(janela, text="Simular", command=iniciar_simulacao)
botao_simular.grid(row=3, column=0, columnspan=2, pady=5)

botao_salvar = tk.Button(janela, text="Salvar Gráfico", command=salvar_grafico)
botao_salvar.grid(row=4, column=0, columnspan=2, pady=5)

fig = plt.figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=janela)
canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, pady=10)

janela.mainloop()
