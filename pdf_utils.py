import PyPDF2
import re
import os
import concurrent.futures
import multiprocessing

def buscar_nome(nome, pdf_path):
    resultados = []
    try:
        with open(pdf_path, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for num_pagina, pagina in enumerate(leitor.pages, start=1):
                texto = pagina.extract_text().lower()
                if re.search(r'\b' + re.escape(nome.lower()) + r'\b', texto):
                    resultados.append(num_pagina)
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {str(e)}")
    return resultados

def buscar_nome_em_pasta(nome, pasta_path):
    resultados = {}
    arquivos_pdf = [f for f in os.listdir(pasta_path) if f.lower().endswith('.pdf')]
    
    num_cores = multiprocessing.cpu_count()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
        futuros = {executor.submit(buscar_nome, nome, os.path.join(pasta_path, arquivo)): arquivo for arquivo in arquivos_pdf}
        for futuro in concurrent.futures.as_completed(futuros):
            arquivo = futuros[futuro]
            try:
                paginas = futuro.result()
                if paginas:
                    resultados[os.path.join(pasta_path, arquivo)] = paginas
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {str(e)}")
    
    return resultados

def extrair_paginas(resultados, pasta_saida, nome_busca):
    merger = PyPDF2.PdfMerger()
    paginas_adicionadas = set()  # Conjunto para rastrear páginas já adicionadas
    
    for arquivo_path, paginas in resultados.items():
        if os.path.exists(arquivo_path):
            try:
                with open(arquivo_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for pagina in paginas:
                        # Cria uma chave única para cada página
                        pagina_key = (arquivo_path, pagina)
                        if pagina_key not in paginas_adicionadas:
                            # Adiciona apenas a página específica
                            pdf_writer = PyPDF2.PdfWriter()
                            pdf_writer.add_page(pdf_reader.pages[pagina-1])
                            
                            # Cria um arquivo temporário para a página
                            with open(f"temp_{arquivo_path.split('/')[-1]}_{pagina}.pdf", 'wb') as temp_file:
                                pdf_writer.write(temp_file)
                            
                            # Adiciona o arquivo temporário ao merger
                            merger.append(f"temp_{arquivo_path.split('/')[-1]}_{pagina}.pdf")
                            paginas_adicionadas.add(pagina_key)
            except Exception as e:
                print(f"Erro ao processar {arquivo_path}: {str(e)}")
        else:
            print(f"Arquivo não encontrado: {arquivo_path}")
    
    nome_arquivo = f"resultado_busca_{nome_busca}.pdf"
    caminho_saida = os.path.join(pasta_saida, nome_arquivo)
    
    if len(paginas_adicionadas) > 0:
        try:
            with open(caminho_saida, 'wb') as output_file:
                merger.write(output_file)
            
            # Remove os arquivos temporários
            for temp_file in [f for f in os.listdir() if f.startswith("temp_") and f.endswith(".pdf")]:
                os.remove(temp_file)
            
            return caminho_saida
        except Exception as e:
            return f"Erro ao salvar o arquivo de saída: {str(e)}"
    else:
        return "Nenhuma página encontrada para extrair."