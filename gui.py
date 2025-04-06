import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from simulator import simular_decaimento_radioativo
from controller import salvar_csv, salvar_grafico, salvar_csv_personalizado, salvar_grafico_personalizado
import os

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

    def abrir_tela_lote():
        lote = Toplevel()
        lote.title("Simulações em Lote")
        lote.configure(padx=15, pady=15)

        tk.Label(lote, text="Taxa Mínima:").grid(row=0, column=0, sticky="w")
        entry_taxa_min = tk.Entry(lote, width=20)
        entry_taxa_min.grid(row=0, column=1)

        tk.Label(lote, text="Taxa Máxima:").grid(row=1, column=0, sticky="w")
        entry_taxa_max = tk.Entry(lote, width=20)
        entry_taxa_max.grid(row=1, column=1)

        tk.Label(lote, text="Qtd Simulações:").grid(row=2, column=0, sticky="w")
        entry_qtd_simulacoes = tk.Entry(lote, width=20)
        entry_qtd_simulacoes.grid(row=2, column=1)

        def executar_lote():
            try:
                qtd_inicial = int(entry_qtd.get())
                taxa_min = float(entry_taxa_min.get())
                taxa_max = float(entry_taxa_max.get())
                duracao = int(entry_anos.get())
                num_simulacoes = int(entry_qtd_simulacoes.get())

                if not (0 < taxa_min < taxa_max < 1):
                    raise ValueError("A faixa de taxa deve estar entre 0 e 1.")

                pasta = filedialog.askdirectory(title="Escolha a pasta para salvar os resultados")
                if not pasta:
                    return

                for i in range(num_simulacoes):
                    taxa_atual = taxa_min + i * ((taxa_max - taxa_min) / max(1, num_simulacoes - 1))
                    tempos, quantidades, _ = simular_decaimento_radioativo(qtd_inicial, taxa_atual, duracao)
                    nome_base = f"sim_{i+1}_taxa_{round(taxa_atual, 3)}"
                    salvar_csv_personalizado(tempos, quantidades, os.path.join(pasta, f"{nome_base}.csv"))
                    salvar_grafico_personalizado(tempos, quantidades, os.path.join(pasta, f"{nome_base}.png"))

                messagebox.showinfo("Sucesso", f"{num_simulacoes} simulações salvas com sucesso em:\n{pasta}")
                lote.destroy()

            except ValueError as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(lote, text="Executar Lote", bg="#007F5F", fg="white", command=executar_lote).grid(row=3, column=0, columnspan=2, pady=15)

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

    tk.Label(frame_inputs, text="Duração (anos):").grid(row=2, column=0, sticky="w")
    entry_anos = tk.Entry(frame_inputs, width=25)
    entry_anos.grid(row=2, column=1, pady=5)

    tk.Button(frame_inputs, text="Simular", width=20, bg="#5A189A", fg="white", command=iniciar_simulacao).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(frame_inputs, text="Salvar Gráfico", width=20, command=lambda: salvar_grafico(fig)).grid(row=4, column=0, columnspan=2, pady=5)
    tk.Button(frame_inputs, text="Salvar CSV", width=20, command=lambda: salvar_csv(estado["dados_csv"])).grid(row=5, column=0, columnspan=2, pady=5)
    tk.Button(frame_inputs, text="Simulações em Lote", width=20, bg="#007F5F", fg="white", command=abrir_tela_lote).grid(row=6, column=0, columnspan=2, pady=10)

    frame_visual = tk.Frame(janela)
    frame_visual.grid(row=0, column=1, padx=20)

    global fig, canvas, text_logs
    fig = plt.figure(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=frame_visual)
    canvas.get_tk_widget().pack()

    text_logs = tk.Text(frame_visual, height=10, width=50, state='disabled', bg="#F5F5F5")
    text_logs.pack(pady=10)

    janela.mainloop()
