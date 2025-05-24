import streamlit as st
import json
import smtplib
from email.message import EmailMessage
from datetime import datetime

st.set_page_config(page_title="Setor de Agrupamento - Grupo Reobote Serviços")

st.title("Setor de Agrupamento - Grupo Reobote Serviços")

if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.data = {}

# Função para enviar e-mail com os dados
def enviar_email(dados):
    msg = EmailMessage()
    msg['Subject'] = 'Novo preenchimento - Grupo Reobote Serviços'
    msg['From'] = 'seuemail@gmail.com'
    msg['To'] = 'gruporeoboteofc@gmail.com'

    corpo = json.dumps(dados, indent=2, ensure_ascii=False)
    msg.set_content(f"Preenchimento de cliente:\n\n{corpo}")

    # Adiciona anexo JSON
    json_bytes = json.dumps(dados, ensure_ascii=False).encode('utf-8')
    msg.add_attachment(json_bytes, maintype='application', subtype='json', filename='dados_cliente.json')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('seuemail@gmail.com', 'suasenha')
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")
        return False

# Etapas do chatbot
if st.session_state.step == 1:
    nome = st.text_input("Olá! Qual o seu nome?")
    if st.button("Enviar nome") and nome:
        st.session_state.data['nome'] = nome
        st.session_state.step = 2

elif st.session_state.step == 2:
    cidade = st.text_input("Qual a sua cidade?")
    estado = st.text_input("E seu estado?")
    if st.button("Enviar localização") and cidade and estado:
        st.session_state.data['cidade'] = cidade
        st.session_state.data['estado'] = estado
        st.session_state.step = 3

elif st.session_state.step == 3:
    servico = st.radio("Qual serviço você deseja?", ("Parceria", "Vínculo de assessoria", "Agendar com artista"))
    if st.button("Escolher serviço"):
        st.session_state.data['servico'] = servico
        if servico == "Agendar com artista":
            st.session_state.step = 4.1
        else:
            st.session_state.step = 5

elif st.session_state.step == 4.1:
    data_evento = st.date_input("Data do evento")
    hora_inicio = st.time_input("Hora de início")
    hora_fim = st.time_input("Hora de término")
    if st.button("Confirmar horário"):
        st.session_state.data['data_evento'] = str(data_evento)
        st.session_state.data['hora_inicio'] = str(hora_inicio)
        st.session_state.data['hora_fim'] = str(hora_fim)
        st.session_state.step = 5

elif st.session_state.step == 5:
    telefone = st.text_input("Informe seu telefone para contato")
    email = st.text_input("E seu e-mail?")
    if st.button("Finalizar e enviar"):
        st.session_state.data['telefone'] = telefone
        st.session_state.data['email'] = email
        enviado = enviar_email(st.session_state.data)
        if enviado:
            st.success("Dados enviados com sucesso! Em breve entraremos em contato.")
            st.session_state.step = 6

# Tela final opcional de login do administrador
elif st.session_state.step == 6:
    if st.checkbox("Área administrativa (somente administradores)"):
        usuario = st.text_input("Usuário", key="admin_user")
        senha = st.text_input("Senha", type="password", key="admin_pass")
        if st.button("Entrar como administrador"):
            if usuario == "admin" and senha == "1234":
                st.success("Login realizado com sucesso! (em desenvolvimento)")
                st.info("Aqui será exibido o painel do administrador para cadastrar artistas, preços e visualizar dados.")
            else:
                st.error("Usuário ou senha incorretos.")
    
