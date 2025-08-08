
import streamlit as st
from docx import Document
import requests
import io

st.set_page_config(page_title="Gerador de Contrato de Honorários", layout="centered")

st.title("📄 Gerador de Contrato de Honorários")
st.markdown("Preencha os dados abaixo para gerar automaticamente o contrato personalizado.")

# === FORMULÁRIO ===
with st.form("form_contrato"):
    nome = st.text_input("Nome do contratante")
    cpf = st.text_input("CPF")
    endereco = st.text_input("Endereço")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")
    resumo_acao = st.text_area("Resumo da Ação (será inserido entre aspas no contrato)", height=150)
    gerar = st.form_submit_button("Gerar Contrato")

# === LINK DO ARQUIVO ===
dropbox_link = "https://www.dropbox.com/scl/fi/b7ye092nuy4i35r8bpwi0/CONTRATO-HONORARIOS.docx?rlkey=vx1l2sbwmue3u47etfr1nnejk&dl=1"

# === LÓGICA DE GERAÇÃO ===
def preencher_contrato(template, dados, resumo):
    for p in template.paragraphs:
        for chave, valor in dados.items():
            if chave in p.text:
                p.text = p.text.replace(chave, valor)
        if '""' in p.text:
            p.text = p.text.replace('""', resumo)
    return template

if gerar:
    if not all([nome, cpf, endereco, telefone, email, resumo_acao]):
        st.error("Por favor, preencha todos os campos.")
    else:
        # Baixar o contrato do Dropbox
        res = requests.get(dropbox_link)
        doc = Document(io.BytesIO(res.content))

        # Dados para substituir no contrato
        dados_contratante = {
            "NOME": nome,
            "CPF": cpf,
            "ENDERECO": endereco,
            "TELEFONE": telefone,
            "EMAIL": email
        }

        contrato_final = preencher_contrato(doc, dados_contratante, resumo_acao)

        # Salvar em memória
        buffer = io.BytesIO()
        contrato_final.save(buffer)
        buffer.seek(0)

        st.success("✅ Contrato gerado com sucesso!")
        st.download_button(
            label="📥 Baixar Contrato",
            data=buffer,
            file_name="Contrato_Honorarios_Preenchido.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
