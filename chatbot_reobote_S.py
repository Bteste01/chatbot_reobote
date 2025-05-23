# chatbot_reobote_servicos.py
import streamlit as st
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from datetime import datetime

st.set_page_config(page_title="Setor de Agrupamento - Grupo Reobote Serviços")

st.title("Setor de Agrupamento - Grupo Reobote Serviços")

# Sessão inicial
if 'step' not in st.session_state:
    st.session_state.update({
        'step': 0,
        'nome': '',
        'cidade': '',
        'estado': '',
        'servico': '',
        'dados': {},
        'admin': False,
        'tipo_admin': ''
    })

# Função para salvar e enviar email
def salvar_e_enviar_email(dados):
    filename = f"dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(dados, f, indent=2)

    msg = MIMEMultipart()
    msg['From'] = 'seuemail@gmail.com'  # configure aqui
    msg['To'] = 'gruporeoboteofc@gmail.com'
    msg['Subject'] = f"Novo Formulário - {dados.get('nome')}"

    body = "".join([f"{k}: {v}\n" for k, v in dados.items()])
    msg.attach(MIMEText(body, 'plain'))

    with open(filename, "rb") as f:
        part = MIMEApplication(f.read(), Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('seuemail@gmail.com', 'suasenha')  # configure aqui
        server.send_message(msg)
        server.quit()
        os.remove(filename)
        return True
    except Exception as e:
        st.error("Erro ao enviar e-mail")
        return False

# Etapas do chatbot
if st.session_state.step == 0:
    st.write("Olá! Qual seu nome?")
    nome = st.text_input("Nome")
    if st.button("Enviar") and nome:
        st.session_state.nome = nome
        st.session_state.step = 1

elif st.session_state.step == 1:
    cidade = st.text_input("Cidade")
    if st.button("Enviar cidade") and cidade:
        st.session_state.cidade = cidade
        st.session_state.step = 2

elif st.session_state.step == 2:
    estado = st.text_input("Estado")
    if st.button("Enviar estado") and estado:
        st.session_state.estado = estado
        st.session_state.step = 3

elif st.session_state.step == 3:
    st.write("Qual serviço deseja?")
    servico = st.radio("Serviço", ["Parceria", "Vínculo de assessoria", "Agendar com artista"])
    if st.button("Escolher serviço"):
        st.session_state.servico = servico
        st.session_state.step = 4

elif st.session_state.step == 4:
    dados = {
        "nome": st.session_state.nome,
        "cidade": st.session_state.cidade,
        "estado": st.session_state.estado,
        "servico": st.session_state.servico
    }

    if st.session_state.servico == "Agendar com artista":
        artista = st.text_input("Nome do artista")
        preco = st.text_input("Preço combinado")
        data_evento = st.date_input("Data do evento")
        hora_inicio = st.time_input("Hora de início")
        hora_termo = st.time_input("Hora de término")
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")
        if st.button("Salvar e Enviar"):
            dados.update({
                "artista": artista,
                "preco": preco,
                "data_evento": str(data_evento),
                "hora_inicio": str(hora_inicio),
                "hora_termo": str(hora_termo),
                "telefone": telefone,
                "email": email
            })
            st.session_state.dados = dados
            if salvar_e_enviar_email(dados):
                st.success("Dados enviados com sucesso!")
                st.session_state.step = 0
    else:
        prazo = st.selectbox("Prazo do contrato", ["3 meses", "6 meses", "12 meses"])
        forma_pagamento = st.selectbox("Forma de pagamento", ["Pix", "Cartão", "Boleto"])
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")
        if st.button("Salvar e Enviar"):
            dados.update({
                "prazo": prazo,
                "forma_pagamento": forma_pagamento,
                "telefone": telefone,
                "email": email
            })
            st.session_state.dados = dados
            if salvar_e_enviar_email(dados):
                st.success("Dados enviados com sucesso!")
                st.session_state.step = 0

# Área administrativa
st.sidebar.title("Área Administrativa")
admin_user = st.sidebar.text_input("Usuário")
admin_pass = st.sidebar.text_input("Senha", type="password")

if st.sidebar.button("Entrar"):
    if admin_user == "admin" and admin_pass == "1234":
        st.session_state.admin = True
        st.session_state.tipo_admin = "principal"
    elif admin_user == "comum" and admin_pass == "1234":
        st.session_state.admin = True
        st.session_state.tipo_admin = "comum"
    else:
        st.sidebar.error("Acesso negado")

if st.session_state.admin:
    st.sidebar.success(f"Logado como {st.session_state.tipo_admin}")
    st.subheader("Gerenciar Artistas")

    if 'artistas' not in st.session_state:
        st.session_state.artistas = []

    novo_artista = st.text_input("Nome do artista para cadastrar")
    preco_artista = st.text_input("Preço do artista")
    if st.button("Cadastrar Artista") and novo_artista and preco_artista:
        st.session_state.artistas.append({"nome": novo_artista, "preco": preco_artista})
        st.success("Artista cadastrado")

    if st.session_state.artistas:
        for i, artista in enumerate(st.session_state.artistas):
            st.write(f"{artista['nome']} - R$ {artista['preco']}")
            if st.button(f"Excluir {artista['nome']}"):
                st.session_state.artistas.pop(i)
                st.experimental_rerun()
    
