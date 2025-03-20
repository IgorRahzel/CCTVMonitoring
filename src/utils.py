import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def generate_person_report(csv_file, output_pdf):
    '''
    Gera um relatório em PDF a partir de um arquivo CSV de uma pessoa.
    O relatório contém:
    - Gráfico comparando as atividades realizadas em cada área.
    - Tempo total gasto em cada área.
    - Tempo total gasto em cada ação.
    '''
    # Ler o arquivo CSV
    df = pd.read_csv(csv_file)

    # Verificar se o CSV tem o formato esperado
    if 'Área' not in df.columns:
        raise ValueError("O arquivo CSV não contém a coluna 'Área'.")

    # Calcular o tempo total gasto em cada área
    df['Tempo Total na Área'] = df.iloc[:, 1:].sum(axis=1)  # Soma das colunas de ações

    # Calcular o tempo total gasto em cada ação
    action_totals = df.iloc[:, 1:-1].sum()  # Soma das linhas para cada ação

    # Criar gráfico comparativo
    plt.figure(figsize=(10, 6))
    df.set_index('Área').iloc[:, :-1].plot(kind='bar', stacked=True, colormap='viridis')
    plt.title('Atividades Realizadas em Cada Área')
    plt.xlabel('Área')
    plt.ylabel('Tempo (frames)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvar o gráfico como uma imagem temporária
    graph_image = "temp_graph.png"
    plt.savefig(graph_image)
    plt.close()

    # Criar o PDF
    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, 750, f"Relatório de Atividades - {os.path.basename(csv_file)}")

    # Adicionar o gráfico ao PDF
    pdf.setFont("Helvetica", 12)
    pdf.drawString(72, 730, "Gráfico de Atividades por Área:")
    pdf.drawImage(ImageReader(graph_image), 72, 500, width=450, height=200)

    # Adicionar o tempo total gasto em cada área
    pdf.drawString(72, 450, "Tempo Total Gasto em Cada Área:")
    y = 430
    for index, row in df.iterrows():
        pdf.drawString(72, y, f"{row['Área']}: {row['Tempo Total na Área']} frames")
        y -= 15

    # Adicionar o tempo total gasto em cada ação
    pdf.drawString(72, y - 20, "Tempo Total Gasto em Cada Ação:")
    y -= 40
    for action, total in action_totals.items():
        pdf.drawString(72, y, f"{action}: {total} frames")
        y -= 15

    # Finalizar o PDF
    pdf.save()

    # Remover a imagem temporária do gráfico
    os.remove(graph_image)

    print(f"Relatório gerado com sucesso: {output_pdf}")

def generate_reports_from_csv(input_dir, output_dir):
    '''
    Gera relatórios em PDF para todos os arquivos CSV em um diretório de entrada
    e salva os PDFs em um diretório de saída.
    '''
    # Verificar se o diretório de entrada existe
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Diretório de entrada não encontrado: {input_dir}")

    # Criar o diretório de saída, se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Iterar sobre todos os arquivos CSV no diretório de entrada
    for csv_file in os.listdir(input_dir):
        if csv_file.endswith(".csv"):
            csv_path = os.path.join(input_dir, csv_file)
            pdf_file = os.path.join(output_dir, f"{os.path.splitext(csv_file)[0]}_report.pdf")
            generate_person_report(csv_path, pdf_file)