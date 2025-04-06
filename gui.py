import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from simulator import simular_decaimento_radioativo
from controller import salvar_csv, salvar_grafico

def iniciar_interface():
    estado = {"dados_csv": []}

    def iniciar_simulacao():
        try:
            qtd_inicial = int(entry_qtd.get())
            taxa_decaimento = float(entry_taxa.get())
            duracao = int(entry_anos.get())

            if not (0 < taxa_decaimento < 1):
                raise ValueError("A taxa de decaimento deve estar entre 0 e 1.")

            tempos, quantidades, log = simular_decaimento_radioativo(qtd_inicial, taxa_decaimento, duracao)
            exibir_grafico(tempos, quantidades)
            atualizar_logs(log)
            estado["dados_csv"] = list(zip(tempos, quantidades))

        except ValueError as e:
            messagebox.showerror("Erro de entrada", str(e))

    def exibir_grafico(tempos, quantidades):
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

    def atualizar_logs(logs):
        text_logs.config(state='normal')
        text_logs.delete(1.0, tk.END)
        for linha in logs:
            text_logs.insert(tk.END, linha + "\n")
        text_logs.config(state='disabled')

    janela = tk.Tk()
    janela.title("Simulador de Decaimento Radioativo")
    janela.configure(padx=20, pady=20)

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

    tk.Button(frame_inputs, text="Simular", width=20, bg="#5A189A", fg="white", command=iniciar_simulacao).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(frame_inputs, text="Salvar Gráfico", width=20, command=lambda: salvar_grafico(fig)).grid(row=4, column=0, columnspan=2, pady=5)
    tk.Button(frame_inputs, text="Salvar CSV", width=20, command=lambda: salvar_csv(estado["dados_csv"])).grid(row=5, column=0, columnspan=2, pady=5)

    frame_visual = tk.Frame(janela)
    frame_visual.grid(row=0, column=1, padx=20)

    global fig, canvas, text_logs
    fig = plt.figure(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=frame_visual)
    canvas.get_tk_widget().pack()

    text_logs = tk.Text(frame_visual, height=10, width=50, state='disabled', bg="#F5F5F5")
    text_logs.pack(pady=10)

    janela.mainloop()
