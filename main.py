import PyPDF2
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Função para buscar o nome no PDF e retornar as páginas onde ele está presente
def buscar_nome(nome, pdf_path):
    # Abre o arquivo PDF
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        paginas_encontradas = []

        # Loop pelas páginas do PDF
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            texto = page.extract_text()
            
            # Busca o nome (case-insensitive) na página
            if re.search(r'\b' + re.escape(nome) + r'\b', texto, re.IGNORECASE):
                paginas_encontradas.append(page_num + 1)  # Páginas começam em 1

        return paginas_encontradas

# Função para abrir o diálogo de seleção de arquivo
def selecionar_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, file_path)

# Função para buscar o nome no PDF e mostrar o resultado
def buscar():
    print("Função buscar iniciada")
    nome = entry_nome.get().strip()
    pdf_path = entry_pdf.get().strip()
    
    if not nome:
        messagebox.showerror("Erro", "Por favor, insira o nome a ser buscado.")
        return
    if not pdf_path:
        messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF.")
        return
    
    label_resultado.config(text="Buscando, por favor, aguarde...")
    root.update()
    
    try:
        paginas = buscar_nome(nome, pdf_path)
        
        if paginas:
            resultado = f"Nome '{nome}' encontrado nas páginas: {', '.join(map(str, paginas))}"
        else:
            resultado = f"Nome '{nome}' não encontrado no PDF."
        
        print(f"Resultado da busca: {resultado}")  # Adicione esta linha para debug
        label_resultado.config(text=resultado)
        root.update()  # Adicione esta linha para forçar a atualização da interface
    except Exception as e:
        erro = f"Ocorreu um erro durante a busca: {str(e)}"
        print(f"Erro: {erro}")  # Adicione esta linha para debug
        messagebox.showerror("Erro", erro)
        label_resultado.config(text="Erro durante a busca.")
        root.update()  # Adicione esta linha para forçar a atualização da interface
    
    print("Função buscar concluída")

# Criando a interface gráfica
root = tk.Tk()
root.title("Busca de Nomes no PDF")

# Configurando a janela
root.geometry("400x200")

# Nome a ser buscado
tk.Label(root, text="Nome a ser buscado:").pack(pady=5)
entry_nome = tk.Entry(root, width=40)
entry_nome.pack()

# Selecionar PDF
tk.Label(root, text="Selecione o PDF:").pack(pady=5)
entry_pdf = tk.Entry(root, width=40)
entry_pdf.pack()

btn_pdf = tk.Button(root, text="Selecionar PDF", command=selecionar_pdf)
btn_pdf.pack(pady=5)

# Botão para buscar
btn_buscar = tk.Button(root, text="Buscar", command=buscar)
btn_buscar.pack(pady=10)

# Label de resultado
label_resultado = tk.Label(root, text="", wraplength=380)  # Adicione wraplength
label_resultado.pack(pady=5, padx=10)  # Adicione padx

# Executar a interface
root.mainloop()

print("Interface iniciada")
