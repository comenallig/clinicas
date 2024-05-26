import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Instala o PyPDF2
install("PyPDF2")

import PyPDF2
import pandas as pd
 
# Load your PDF file
file_path = "/Users/julio/Downloads/ConsultarExtrato.pdf"
pdf_file = open(file_path, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
 
# Extract text from the PDF
pages_text = [page.extract_text() for page in pdf_reader.pages if page.extract_text() is not None]
 
# Convert the list of texts to a DataFrame
df = pd.DataFrame(pages_text, columns=['text'])
 
# Split the text into separate lines
df = df['text'].apply(lambda x: x.split('\n')).explode('text').reset_index(drop=True).to_frame()
 
# Filter rows containing "2023 |"
df_filtered = df[df['text'].str.contains("2023 \| [^|]+")]
 
# Extract names after "2023 |"
df_filtered['nomes'] = df_filtered['text'].str.extract(r"(?<=2023 \| )[^|]+")
 
# Trim whitespace from the 'nomes' column
df_filtered['nomes'] = df_filtered['nomes'].str.strip()
 
# Select only the 'nomes' column
df_final = df_filtered[['nomes']]
 
# Print the final DataFrame
print(df_final)
