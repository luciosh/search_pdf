import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_utils import buscar_nome_em_pasta, extrair_paginas
import time
import os

class BuscaNomesPDFApp:
    def __init__(self, master):
        self.master = master
        master.title("Busca de Nomes no PDF")
        master.geometry("400x600")

        self.criar_widgets()

    def criar_widgets(self):
        # Nome a ser buscado
        tk.Label(self.master, text="Nome a ser buscado:").pack(pady=5)
        self.entry_nome = tk.Entry(self.master, width=40)
        self.entry_nome.pack()

        # Selecionar pasta
        tk.Label(self.master, text="Selecione a pasta com PDFs:").pack(pady=5)
        self.entry_pdf = tk.Entry(self.master, width=40)
        self.entry_pdf.pack()

        btn_pdf = tk.Button(self.master, text="Selecionar Pasta", command=self.selecionar_pasta)
        btn_pdf.pack(pady=5)

        # Selecionar pasta de saída
        tk.Label(self.master, text="Selecione a pasta de saída:").pack(pady=5)
        self.entry_saida = tk.Entry(self.master, width=40)
        self.entry_saida.pack()

        btn_saida = tk.Button(self.master, text="Selecionar Pasta de Saída", command=self.selecionar_pasta_saida)
        btn_saida.pack(pady=5)

        # Botão para buscar
        btn_buscar = tk.Button(self.master, text="Buscar", command=self.buscar)
        btn_buscar.pack(pady=10)

        # Criando um widget Text para exibir os resultados com barra de rolagem
        self.text_resultado = tk.Text(self.master, wrap=tk.WORD, height=10, width=50)
        self.text_resultado.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Adicionando uma barra de rolagem ao widget Text
        scrollbar = tk.Scrollbar(self.master, command=self.text_resultado.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_resultado.config(yscrollcommand=scrollbar.set)

    def selecionar_pasta(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.entry_pdf.delete(0, tk.END)
            self.entry_pdf.insert(0, folder_path)

    def selecionar_pasta_saida(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.entry_saida.delete(0, tk.END)
            self.entry_saida.insert(0, folder_path)

    def buscar(self):
        print("Função buscar iniciada")
        nome = self.entry_nome.get().strip()
        pasta_path = os.path.abspath(self.entry_pdf.get().strip())
        pasta_saida = os.path.abspath(self.entry_saida.get().strip())
        
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira o nome a ser buscado.")
            return
        if not pasta_path:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta com PDFs.")
            return
        if not pasta_saida:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta de saída.")
            return
        
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(tk.END, "Buscando, por favor, aguarde...")
        self.master.update()
        
        tempo_inicio = time.time()
        
        try:
            resultados = buscar_nome_em_pasta(nome, pasta_path)
            
            tempo_fim = time.time()
            tempo_total = tempo_fim - tempo_inicio
            
            if resultados:
                texto_resultado = f"Nome '{nome}' encontrado nos seguintes arquivos:\n\n"
                total_paginas = 0
                for arquivo_path, paginas in resultados.items():
                    nome_arquivo = os.path.basename(arquivo_path)
                    texto_resultado += f"{nome_arquivo}: páginas {', '.join(map(str, paginas))}\n"
                    total_paginas += len(set(paginas))  # Conta apenas páginas únicas
                
                caminho_saida = extrair_paginas(resultados, pasta_saida, nome)
                if caminho_saida.startswith("Nenhuma página"):
                    texto_resultado += f"\n{caminho_saida}"
                else:
                    nome_arquivo_saida = os.path.basename(caminho_saida)
                    texto_resultado += f"\nNovo PDF criado: {nome_arquivo_saida}"
                    texto_resultado += f"\nTotal de páginas únicas encontradas: {total_paginas}"
            else:
                texto_resultado = f"Nome '{nome}' não encontrado em nenhum PDF da pasta."
            
            texto_resultado += f"\n\nTempo total de busca: {tempo_total:.2f} segundos"
            
            print(f"Resultado da busca: {texto_resultado}")
            self.text_resultado.delete(1.0, tk.END)
            self.text_resultado.insert(tk.END, texto_resultado)
        except Exception as e:
            tempo_fim = time.time()
            tempo_total = tempo_fim - tempo_inicio
            
            erro = f"Ocorreu um erro durante a busca: {str(e)}\n\nTempo total: {tempo_total:.2f} segundos"
            print(f"Erro: {erro}")
            messagebox.showerror("Erro", erro)
            self.text_resultado.delete(1.0, tk.END)
            self.text_resultado.insert(tk.END, f"Erro durante a busca.\nTempo total: {tempo_total:.2f} segundos")
        
        print("Função buscar concluída")