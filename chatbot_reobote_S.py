import streamlit as st
import json
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

# Funções auxiliares
def carregar_admins():
    if os.path.exists("admin.json"):
        with open("admin.json", "r") as f:
            return json.load(f)
    return []

def salvar_artistas(artistas):
    with open("artistas.json", "w") as f:
        json.dump(artistas, f)

def carregar_artistas():
    if os.path.exists("artistas.json"):
        with open("artistas.json", "r") as f:
            return json.load(f)
    return []

def salvar_cliente(dados):
    nome_arquivo = f"{dados['nome'].replace(' ', '_')}_{datetime.now().isoformat()}.json"
    with open(nome_arquivo, "w") as f:
        json.dump(dados, f)

    # Enviar e-mail
    msg = EmailMessage()
    msg["Subject"] = f"Novo contrato de {dados['nome']}"
    msg["From"] = "seuemail@gmail.com"
    msg["To"] = "gruporeoboteofc@gmail.com"
    corpo = "\n".join(f"{k}: {v}" for k, v in dados.items())
    msg.set_content(corpo)

    with open(nome_arquivo, "rb") as f:
        msg.add_attachment(f.read(), filename=nome_arquivo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("seuemail@gmail.com", "sua_senha")
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")

# Interface de login
def login():
    st.title("Setor de Agrupamento - Grupo Reobote Serviços")
    st.subheader("Login do Administrador")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        admins = carregar_admins()
        for admin in admins:
            if admin["usuario"] == usuario and admin["senha"] == senha:
                st.session_state["logado"] = True
                st.session_state["tipo"] = admin["tipo"]
                st.session_state["usuario"] = usuario
                st.experimental_rerun()
        st.error("Usuário ou senha inválidos.")

# Interface do painel administrativo
def painel_administrador():
    st.sidebar.success(f"Logado como: {st.session_state['usuario']} ({st.session_state['tipo']})")
    aba = st.sidebar.radio("Menu", ["Cadastro de Artistas", "Visualizar Dados"])

    if aba == "Cadastro de Artistas" and st.session_state["tipo"] == "principal":
        st.subheader("Cadastrar Novo Artista")
        nome = st.text_input("Nome do artista")
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        if st.button("Salvar artista"):
            artistas = carregar_artistas()
            artistas.append({"nome": nome, "preco": preco})
            salvar_artistas(artistas)
            st.success("Artista cadastrado com sucesso!")

        st.subheader("Excluir Artistas")
        artistas = carregar_artistas()
        nomes = [a["nome"] for a in artistas]
        nome_excluir = st.selectbox("Selecionar artista", nomes)
        if st.button("Excluir artista"):
            artistas = [a for a in artistas if a["nome"] != nome_excluir]
            salvar_artistas(artistas)
            st.success("Artista excluído!")

    elif aba == "Visualizar Dados":
        st.subheader("Acompanhamento dos contratos")
        arquivos = [f for f in os.listdir() if f.endswith(".json") and "artistas" not in f and "admin" not in f]
        for arq in arquivos:
            with open(arq) as f:
                dados = json.load(f)
                with st.expander(arq):
                    st.json(dados)

# Interface do chatbot (clientes)
def chatbot():
    st.title("Setor de Agrupamento - Grupo Reobote Serviços")
    st.subheader("Inicie seu atendimento")

    with st.form("form_chat"):
        nome = st.text_input("Seu nome")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        servico = st.selectbox("Serviço desejado", ["Parceria", "Vínculo de assessoria", "Agendar com artista"])
        
        artista_escolhido = None
        if servico == "Agendar com artista":
            artistas = carregar_artistas()
            nomes = [a["nome"] for a in artistas]
            artista_escolhido = st.selectbox("Escolher artista", nomes)
            data_evento = st.date_input("Data do evento")
            hora_inicio = st.time_input("Hora de início")
            hora_fim = st.time_input("Hora de término")
        
        prazo = None
        if servico in ["Parceria", "Vínculo de assessoria"]:
            prazo = st.selectbox("Prazo do contrato", ["3 meses", "6 meses", "12 meses"])

        email = st.text_input("E-mail para contato")
        telefone = st.text_input("WhatsApp para contato")

        enviado = st.form_submit_button("Enviar")
        if enviado:
            dados = {
                "nome": nome, "cidade": cidade, "estado": estado,
                "servico": servico, "prazo": prazo,
                "artista": artista_escolhido,
                "data_evento": str(data_evento) if servico == "Agendar com artista" else None,
                "hora_inicio": str(hora_inicio) if servico == "Agendar com artista" else None,
                "hora_fim": str(hora_fim) if servico == "Agendar com artista" else None,
                "email": email, "telefone": telefone
            }
            salvar_cliente(dados)
            st.success("Seus dados foram enviados com sucesso!")

# Execução
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if st.session_state["logado"]:
    painel_administrador()
else:
    chatbot()
    st.divider()
    login()
