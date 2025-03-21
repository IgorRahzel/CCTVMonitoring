import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import shutil

def generate_person_report(csv_file, output_pdf):
    '''
    Gera um relatório em PDF a partir de um arquivo CSV de uma pessoa.
    O relatório contém:
    - Gráfico comparando as atividades realizadas em cada área.
    - Gráfico do tempo total gasto em cada área.
    - Gráfico do tempo total gasto em cada ação.
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

    # Criar gráficos
    images = {}

    # Gráfico de atividades realizadas por área
    plt.figure(figsize=(10, 6))
    df.set_index('Área').iloc[:, :-1].plot(kind='bar', stacked=True, colormap='viridis')
    plt.title('Atividades Realizadas em Cada Área')
    plt.xlabel('Área')
    plt.ylabel('Tempo (frames)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    images["activities"] = "activities.png"
    plt.savefig(images["activities"])
    plt.close('all')  # Fecha a figura após salvar

    # Gráfico do tempo total gasto em cada área
    plt.figure(figsize=(8, 5))
    df.plot(x='Área', y='Tempo Total na Área', kind='bar', color='blue', legend=False)
    plt.title('Tempo Total Gasto em Cada Área')
    plt.xlabel('Área')
    plt.ylabel('Tempo (frames)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    images["time_areas"] = "time_areas.png"
    plt.savefig(images["time_areas"])
    plt.close('all')  # Fecha a figura após salvar

    # Gráfico do tempo total gasto em cada ação
    plt.figure(figsize=(8, 5))
    action_totals.plot(kind='bar', color='green', legend=False)
    plt.title('Tempo Total Gasto em Cada Ação')
    plt.xlabel('Ação')
    plt.ylabel('Tempo (frames)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    images["time_actions"] = "time_actions.png"
    plt.savefig(images["time_actions"])
    plt.close('all')  # Fecha a figura após salvar

    # Criar o PDF
    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, 750, f"Relatório de Atividades - {os.path.basename(csv_file)}")

    y_position = 720
    for title, image in [
        ("Gráfico de Atividades por Área", images["activities"]),
        ("Tempo Total Gasto em Cada Área", images["time_areas"]),
        ("Tempo Total Gasto em Cada Ação", images["time_actions"])
    ]:
        pdf.setFont("Helvetica", 12)
        pdf.drawString(72, y_position, title)
        y_position -= 20
        pdf.drawImage(ImageReader(image), 72, y_position - 200, width=450, height=200)
        y_position -= 220

    # Finalizar o PDF
    pdf.save()

    # Remover imagens temporárias
    for img in images.values():
        os.remove(img)

    print(f"Relatório gerado com sucesso: {output_pdf}")


def generate_area_report(csv_file, output_pdf):
    '''
    Gera um relatório em PDF a partir de um arquivo CSV de áreas.
    O relatório contém:
    - Gráfico do número total de pessoas em cada área.
    - Gráfico do tempo total gasto em cada ação por área.
    '''
    # Ler o arquivo CSV
    df = pd.read_csv(csv_file)

    # Verificar se o CSV tem o formato esperado
    if 'Àreas' not in df.columns:
        raise ValueError("O arquivo CSV não contém a coluna 'Àreas'.")

    # Criar gráficos
    images = {}

    # Gráfico do número total de pessoas em cada área
    plt.figure(figsize=(10, 6))
    df.plot(x='Àreas', y='Número Total de Pessoas', kind='bar', color='blue', legend=False)
    plt.title('Número Total de Pessoas em Cada Área')
    plt.xlabel('Área')
    plt.ylabel('Número de Pessoas')
    plt.xticks(rotation=45)
    plt.tight_layout()
    images["total_people"] = "total_people.png"
    plt.savefig(images["total_people"])
    plt.close()

    # Gráfico do tempo total gasto em cada ação por área
    plt.figure(figsize=(10, 6))
    df.set_index('Àreas').iloc[:, 1:].plot(kind='bar', stacked=True, colormap='viridis')
    plt.title('Tempo Total Gasto em Cada Ação por Área')
    plt.xlabel('Área')
    plt.ylabel('Tempo (frames)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    images["time_actions_per_area"] = "time_actions_per_area.png"
    plt.savefig(images["time_actions_per_area"])
    plt.close()

    # Criar o PDF
    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, 750, f"Relatório de Áreas - {os.path.basename(csv_file)}")

    y_position = 720
    for title, image in [
        ("Número Total de Pessoas em Cada Área", images["total_people"]),
        ("Tempo Total Gasto em Cada Ação por Área", images["time_actions_per_area"])
    ]:
        pdf.setFont("Helvetica", 12)
        pdf.drawString(72, y_position, title)
        y_position -= 20
        pdf.drawImage(ImageReader(image), 72, y_position - 200, width=450, height=200)
        y_position -= 220

    # Finalizar o PDF
    pdf.save()

    # Remover imagens temporárias
    for img in images.values():
        os.remove(img)

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

            # Verifica se o arquivo é o areasStats.csv
            if csv_file == "areasStats.csv":
                generate_area_report(csv_path, pdf_file)
            else:
                generate_person_report(csv_path, pdf_file)


# clear stats/ folder
def clear_stats_folder(stats_folder):
    """
    Limpa o conteúdo da pasta stats/ sem excluir a pasta em si.
    :param stats_folder: Caminho para a pasta stats/.
    """
    if os.path.exists(stats_folder):  # Verifica se a pasta existe
        # Remove todo o conteúdo da pasta
        for filename in os.listdir(stats_folder):
            file_path = os.path.join(stats_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove arquivos ou links simbólicos
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove subdiretórios e seu conteúdo
            except Exception as e:
                print(f"Falha ao excluir {file_path}. Razão: {e}")
        print(f"Conteúdo da pasta {stats_folder} limpo com sucesso.")
    else:
        print(f"A pasta {stats_folder} não existe.")


