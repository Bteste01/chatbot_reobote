import streamlit as st
import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Dados iniciais
ADMIN_PRINCIPAL = {"usuario": "admin", "senha": "admin123"}
ADMIN_COMUM = {"user1": "senha1"}
ARTISTAS = {
    "Cantora A": {"preco": 1000},
    "Cantora B": {"preco": 1500},
}

def enviar_email(destinatario, assunto, corpo, anexo_nome, anexo_dados):
    remetente = "seuemail@gmail.com"
    senha = "suasenha"
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))
    part = MIMEApplication(json.dumps(anexo_dados, indent=2), Name=anexo_nome)
    part['Content-Disposition'] = f'attachment; filename="{anexo_nome}"'
    msg.attach(part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            server.send_message(msg)
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")

def salvar_dados(dados):
    with open("dados_clientes.json", "a") as f:
        f.write(json.dumps(dados) + "\n")
    enviar_email(
        "gruporeoboteofc@gmail.com",
        "Novo preenchimento de contrato",
        json.dumps(dados, indent=2),
        "dados.json",
        dados
    )

def chatbot():
    st.title("Setor de Agrupamento - Grupo Reobote Serviços")

    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.dados = {}

    if st.session_state.step == 0:
        st.write("Olá! Qual o seu nome?")
        nome = st.text_input("Digite seu nome")
        if st.button("Enviar", key="nome_btn") and nome:
            st.session_state.dados['nome'] = nome
            st.session_state.step = 1
            st.experimental_rerun()

    elif st.session_state.step == 1:
        cidade = st.text_input("Qual a sua cidade?")
        if st.button("Enviar", key="cidade_btn") and cidade:
            st.session_state.dados['cidade'] = cidade
            st.session_state.step = 2
            st.experimental_rerun()

    elif st.session_state.step == 2:
        estado = st.text_input("Qual o seu estado?")
        if st.button("Enviar", key="estado_btn") and estado:
            st.session_state.dados['estado'] = estado
            st.session_state.step = 3
            st.experimental_rerun()

    elif st.session_state.step == 3:
        servico = st.radio("Qual serviço deseja?", ["Parceria", "Vínculo de assessoria", "Agendar com artista"])
        if st.button("Confirmar serviço"):
            st.session_state.dados['tipo_servico'] = servico
            if servico == "Agendar com artista":
                st.session_state.step = 4.1
            else:
                st.session_state.step = 5
            st.experimental_rerun()

    elif st.session_state.step == 4.1:
        artista = st.selectbox("Escolha o artista:", list(ARTISTAS.keys()))
        data_evento = st.date_input("Data do evento")
        hora_inicio = st.time_input("Hora de início")
        hora_termo = st.time_input("Hora de término")
        if st.button("Confirmar artista e horário"):
            st.session_state.dados.update({
                "artista": artista,
                "preco": ARTISTAS[artista]['preco'],
                "data_evento": str(data_evento),
                "hora_inicio": str(hora_inicio),
                "hora_termo": str(hora_termo)
            })
            st.session_state.step = 5
            st.experimental_rerun()

    elif st.session_state.step == 5:
        email = st.text_input("E-mail para contato")
        telefone = st.text_input("Telefone para contato")
        if st.button("Finalizar"):
            st.session_state.dados.update({"email": email, "telefone": telefone})
            salvar_dados(st.session_state.dados)
            st.success("Dados enviados com sucesso!")
            st.session_state.step = 0
            st.session_state.dados = {}

# Área administrativa
st.sidebar.title("Administração")
if 'admin_tipo' not in st.session_state:
    login_user = st.sidebar.text_input("Usuário")
    login_pass = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if login_user == ADMIN_PRINCIPAL['usuario'] and login_pass == ADMIN_PRINCIPAL['senha']:
            st.session_state.admin_tipo = "principal"
        elif login_user in ADMIN_COMUM and ADMIN_COMUM[login_user] == login_pass:
            st.session_state.admin_tipo = "comum"
        else:
            st.sidebar.error("Credenciais inválidas")
else:
    st.sidebar.success(f"Logado como: {st.session_state.admin_tipo}")
    if st.sidebar.button("Sair"):
        del st.session_state.admin_tipo
        st.experimental_rerun()

    if st.session_state.admin_tipo == "principal":
        st.subheader("Cadastro de novos artistas")
        novo_artista = st.text_input("Nome do artista")
        preco_artista = st.number_input("Preço", min_value=0)
        if st.button("Salvar artista"):
            ARTISTAS[novo_artista] = {"preco": preco_artista}
            st.success("Artista adicionado com sucesso")

        excluir_artista = st.selectbox("Excluir artista", ["Nenhum"] + list(ARTISTAS.keys()))
        if excluir_artista != "Nenhum" and st.button("Excluir"):
            del ARTISTAS[excluir_artista]
            st.success(f"Artista {excluir_artista} excluído.")

# Executa o chatbot se não for admin
if 'admin_tipo' not in st.session_state:
    chatbot()
    
