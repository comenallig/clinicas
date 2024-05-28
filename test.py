pip install PyPDF2 pandas openpyxl

import PyPDF2
import pandas as pd

# Caminho para o arquivo PDF
file_path = "ConsultarExtrato.pdf"

# Abrir o arquivo PDF
with open(file_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extrair texto de todas as páginas do PDF
    pages_text = []
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            # Tentar decodificar o texto em várias codificações comuns
            try:
                decoded_text = text.encode('latin1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                try:
                    decoded_text = text.encode('latin1').decode('iso-8859-1')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    decoded_text = text  # Manter o texto original se a decodificação falhar
            pages_text.append(decoded_text)

# Converter a lista de textos em um DataFrame
df = pd.DataFrame(pages_text, columns=['text'])

# Dividir o texto em linhas separadas
df = df['text'].apply(lambda x: x.split('\n')).explode().reset_index(drop=True).to_frame()

# Filtrar linhas que contêm "2023 |"
df_filtered = df[df['text'].str.contains("2023 \| [^|]+", na=False)].copy()

# Extrair nomes após "2023 |"
df_filtered.loc[:, 'nomes'] = df_filtered['text'].str.extract(r"2023 \| ([^|]+)", expand=False)

# Remover espaços em branco do início e fim da coluna 'nomes'
df_filtered.loc[:, 'nomes'] = df_filtered['nomes'].str.strip()

# Selecionar apenas a coluna 'nomes'
df_final = df_filtered[['nomes']]

# Salvar o DataFrame final em um arquivo Excel
output_file_path = "nomes_extraidos.xlsx"
df_final.to_excel(output_file_path, index=False, encoding='utf-8')

print(f"Os dados foram salvos no arquivo: {output_file_path}")
