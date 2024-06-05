import streamlit as st
import pandas as pd
import PyPDF2
import io
# obs: instalar também as bibliotecas openpyxl e xlsxwriter


def analisa_dados (pdf_file, xlsx_file):
    ## passo 1: lê o arquivo pdf

    # por exemplo:
    # pdf_reader = PyPDF2.PdfReader(pdf_file)
    # text = []
    # for page in pdf_reader.pages:
    #     text.append(page.extract_text())
    # text = "\n".join(text)
    # lines = text.split("\n")
    # df = pd.DataFrame(lines, columns=["content"])
    # return df

    ## passo 2: lê o arquivo xlsx (talvez precise fazer algum ajuste)
    xlsx_df = pd.read_excel(xlsx_file)

    ## passo 3: faz o merge dos dois arquivos
    # por exemplo:
    # joined_df = pd.merge(pdf_df, xlsx_df, on="nome", how="inner")

    # esse código é temporário, só para exemplificar. Substituir
    # pelo resultado do merge
    joined_df = xlsx_df

    return joined_df


st.title("Analisa dados TCU")

pdf_file = st.file_uploader("Upload PDF", type="pdf")

xlsx_file = st.file_uploader("Upload XLSX", type="xlsx")

if st.button("Rodar"):
    if pdf_file and xlsx_file:
        try:
            resultado = analisa_dados(pdf_file, xlsx_file)

            # salva o arquivo em um novo xlsx
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                resultado.to_excel(writer, index=False, sheet_name='Sheet1')
            output.seek(0)
            st.download_button(
                label="Download XLSX final",
                data=output,
                file_name="joined_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload both PDF and XLSX files.")
