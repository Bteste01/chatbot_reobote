import streamlit as st
import json
import smtplib
from email.message import EmailMessage
from datetime import datetime

# Configurações
ADMIN_PRINCIPAL = {"usuario": "admin", "senha": "1234"}
ADMIN_COMUNS = ["comum1", "comum2"]

# Armazenamento local
if "artistas" not in st.session_state:
    st.session_state.artistas = {}
if "dados_clientes" not in st.session_state:
    st.session_state.dados_clientes = []

# Função de envio de e-mail
def enviar_email(dados, destinatario='gruporeoboteofc@gmail.com'):
    msg = EmailMessage()
    msg['Subject'] = 'Novo formulário - Grupo Reobote Serviços'
    msg['From'] = 'seuemail@gmail.com'  # Substituir
    msg['To'] = destinatario

    corpo = "\n".join([f"{k}: {v}" for k, v in dados.items()])
    msg.set_content(corpo)

    json_data = json.dumps(dados, indent=4)
    msg.add_attachment(json_data.encode(), filename='dados.json', maintype='application', subtype='json')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('seuemail@gmail.com', 'senha')  # Substituir por senha segura ou App Password
        smtp.send_message(msg)

# Login
st.title("Setor de Agrupamento - Grupo Reobote Serviços")
menu = st.sidebar.selectbox("Menu", ["Cliente", "Administrador"])

if menu == "Cliente":
    st.subheader("Atendimento Automático")
    nome = st.text_input("Nome completo")
    cidade = st.text_input("Cidade")
    estado = st.text_input("Estado")
    tipo = st.radio("Tipo de serviço", ["Parceria", "Vínculo de assessoria", "Agendar com artista"])

    if tipo == "Agendar com artista":
        artistas = list(st.session_state.artistas.keys()) or ["Nenhum artista cadastrado"]
        artista = st.selectbox("Escolha o artista", artistas)
        data = st.date_input("Data do agendamento")
        hora = st.time_input("Horário")
        preco = st.session_state.artistas.get(artista, "")
        pagamento = st.selectbox("Forma de pagamento", ["Pix", "Cartão", "Dinheiro"])
    elif tipo == "Vínculo de assessoria":
        prazo = st.selectbox("Prazo de contrato", ["3 meses", "6 meses", "12 meses"])
        pagamento = st.selectbox("Forma de pagamento", ["Pix", "Cartão", "Dinheiro"])
    else:
        prazo = ""
        pagamento = ""

    if st.button("Confirmar"):
        dados = {
            "nome": nome, "cidade": cidade, "estado": estado, "tipo": tipo,
            "data": str(data) if tipo == "Agendar com artista" else "",
            "hora": str(hora) if tipo == "Agendar com artista" else "",
            "artista": artista if tipo == "Agendar com artista" else "",
            "preco": preco if tipo == "Agendar com artista" else "",
            "prazo": prazo,
            "pagamento": pagamento
        }
        st.session_state.dados_clientes.append(dados)
        enviar_email(dados)
        st.success("Dados enviados com sucesso!")

elif menu == "Administrador":
    login_user = st.text_input("Usuário")
    login_pass = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if login_user == ADMIN_PRINCIPAL["usuario"] and login_pass == ADMIN_PRINCIPAL["senha"]:
            st.session_state.admin = "principal"
        elif login_user in ADMIN_COMUNS:
            st.session_state.admin = "comum"
        else:
            st.error("Credenciais inválidas")

    if "admin" in st.session_state:
        if st.session_state.admin == "principal":
            st.subheader("Cadastro de Artistas")
            nome_art = st.text_input("Nome do artista")
            preco_art = st.text_input("Preço do artista")
            if st.button("Salvar artista"):
                st.session_state.artistas[nome_art] = preco_art
                st.success("Artista salvo!")
            if st.session_state.artistas:
                del_art = st.selectbox("Deletar artista", list(st.session_state.artistas.keys()))
                if st.button("Deletar artista"):
                    del st.session_state.artistas[del_art]
                    st.success("Artista removido")

        st.subheader("Visualizar dados dos clientes")
        for i, d in enumerate(st.session_state.dados_clientes):
            st.write(f"{i+1}. {d['nome']} - {d['tipo']} - {d.get('artista', '')}")
            with st.expander("Ver detalhes"):
                st.json(d)
    
