pip install pdfplumber-0.5.29-py3-none-any.whl


import pdfplumber
import pandas as pd

# Caminho para o arquivo PDF
file_path = "ConsultarExtrato.pdf"

# Função para decodificar texto
def decode_text(text):
    for encoding in ['utf-8', 'latin1', 'iso-8859-1']:
        try:
            return text.encode('latin1').decode(encoding)
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return text  # Retornar o texto original se todas as decodificações falharem

# Abrir o arquivo PDF
with pdfplumber.open(file_path) as pdf:
    # Extrair texto de todas as páginas do PDF
    pages_text = []
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            decoded_text = decode_text(text)
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
df_final.to_excel(output_file_path, index=False)

print(f"Os dados foram salvos no arquivo: {output_file_path}")
