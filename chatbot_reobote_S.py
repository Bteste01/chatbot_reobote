import streamlit as st
import json
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Função para envio de e-mail com anexo JSON
def enviar_email(dados):
    email_origem = "seuemail@gmail.com"
    senha = "sua_senha"
    email_destino = "gruporeoboteofc@gmail.com"

    msg = EmailMessage()
    msg["Subject"] = "Novo cadastro - Grupo Reobote Serviços"
    msg["From"] = email_origem
    msg["To"] = email_destino

    corpo = "".join([f"{chave}: {valor}\n" for chave, valor in dados.items()])
    msg.set_content(corpo)

    json_data = json.dumps(dados, indent=2).encode("utf-8")
    msg.add_attachment(json_data, maintype="application", subtype="json", filename="dados.json")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_origem, senha)
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")

# Dados de login (simples para exemplo)
admins = {
    "admin_principal": "senha123",
    "admin_comum": "1234"
}

# Sessão do usuário
if 'logado' not in st.session_state:
    st.session_state.logado = False
    st.session_state.tipo_admin = None

st.set_page_config(page_title="Setor de Agrupamento - Grupo Reobote Serviços")
st.title("Setor de Agrupamento - Grupo Reobote Serviços")

# Tela de login
if not st.session_state.logado:
    st.subheader("Login do Administrador")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in admins and senha == admins[usuario]:
            st.session_state.logado = True
            st.session_state.tipo_admin = "principal" if usuario == "admin_principal" else "comum"
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")

# Interface pós login
if st.session_state.logado:
    st.success(f"Bem-vindo, {st.session_state.tipo_admin.upper()}")
    menu = st.sidebar.selectbox("Menu", ["Chatbot Cliente", "Cadastrar Artista", "Ver Dados"])

    if menu == "Cadastrar Artista" and st.session_state.tipo_admin == "principal":
        st.subheader("Cadastro de Artistas")
        nome_artista = st.text_input("Nome do artista")
        preco = st.text_input("Preço do serviço")
        if st.button("Salvar Artista"):
            with open("artistas.json", "a") as f:
                json.dump({"nome": nome_artista, "preco": preco}, f)
                f.write("\n")
            st.success("Artista salvo com sucesso")

    elif menu == "Ver Dados":
        st.subheader("Dados recebidos dos clientes")
        try:
            with open("dados_clientes.json", "r") as f:
                for linha in f:
                    st.json(json.loads(linha))
        except:
            st.warning("Nenhum dado salvo ainda")

    elif menu == "Chatbot Cliente":
        if 'chat_step' not in st.session_state:
            st.session_state.chat_step = 1
            st.session_state.cliente = {}

        def avancar():
            st.session_state.chat_step += 1
            st.experimental_rerun()

        if st.session_state.chat_step == 1:
            nome = st.text_input("Qual seu nome?")
            if st.button("Enviar") and nome:
                st.session_state.cliente["Nome"] = nome
                avancar()

        elif st.session_state.chat_step == 2:
            cidade = st.text_input("Cidade")
            if st.button("Enviar") and cidade:
                st.session_state.cliente["Cidade"] = cidade
                avancar()

        elif st.session_state.chat_step == 3:
            estado = st.text_input("Estado")
            if st.button("Enviar") and estado:
                st.session_state.cliente["Estado"] = estado
                avancar()

        elif st.session_state.chat_step == 4:
            servico = st.radio("Qual serviço deseja?", ["Parceria", "Vínculo de assessoria", "Agendar com artista"])
            if st.button("Enviar"):
                st.session_state.cliente["Serviço"] = servico
                avancar()

        elif st.session_state.chat_step == 5:
            if st.session_state.cliente["Serviço"] == "Agendar com artista":
                data = st.date_input("Data do evento")
                hora_inicio = st.time_input("Hora de início")
                hora_termo = st.time_input("Hora de término")
                if st.button("Confirmar"):
                    st.session_state.cliente["Data do evento"] = str(data)
                    st.session_state.cliente["Início"] = str(hora_inicio)
                    st.session_state.cliente["Término"] = str(hora_termo)
                    avancar()
            else:
                prazo = st.radio("Prazo de contrato", ["3 meses", "6 meses", "12 meses"])
                pagamento = st.text_input("Forma de pagamento")
                if st.button("Confirmar"):
                    st.session_state.cliente["Prazo"] = prazo
                    st.session_state.cliente["Pagamento"] = pagamento
                    avancar()

        elif st.session_state.chat_step == 6:
            email = st.text_input("Seu e-mail")
            telefone = st.text_input("Telefone")
            if st.button("Finalizar"):
                st.session_state.cliente["E-mail"] = email
                st.session_state.cliente["Telefone"] = telefone
                st.session_state.cliente["Data do registro"] = str(datetime.now())

                # Salvar localmente
                with open("dados_clientes.json", "a") as f:
                    json.dump(st.session_state.cliente, f)
                    f.write("\n")

                # Enviar por email
                enviar_email(st.session_state.cliente)

                st.success("Dados enviados com sucesso! Entraremos em contato.")
                st.session_state.chat_step = 1
                st.session_state.cliente = {}
