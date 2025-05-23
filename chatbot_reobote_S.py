import streamlit as st
import json
import hashlib
import smtplib
from email.message import EmailMessage
from datetime import datetime

# ---- ARQUIVOS JSON ----
ARQ_ADMINS = "admins.json"
ARQ_ARTISTAS = "artistas.json"
ARQ_CONTRATOS = "contratos.json"

# ---- USUÁRIOS FIXOS INICIAIS (apenas para rodar primeira vez) ----
# Administrador principal fixo: usuário: admin / senha: admin123
# Administradores comuns são cadastrados via painel admin principal

# --- Funções para JSON ---
def carregar_json(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# --- Função hash para senha ---
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# --- Inicializa arquivos JSON se não existirem ---
def inicializar():
    admins = carregar_json(ARQ_ADMINS)
    if not admins:
        # cria admin principal fixo
        admins["admin"] = {"senha": hash_senha("admin123"), "tipo": "principal"}
        salvar_json(ARQ_ADMINS, admins)
    if not carregar_json(ARQ_ARTISTAS):
        salvar_json(ARQ_ARTISTAS, {})
    if not carregar_json(ARQ_CONTRATOS):
        salvar_json(ARQ_CONTRATOS, {})

# --- Função para enviar email ---
def enviar_email(para_email, assunto, corpo, anexo_json):
    try:
        msg = EmailMessage()
        msg['Subject'] = assunto
        msg['From'] = "seuemail@gmail.com"   # Troque pelo seu e-mail
        msg['To'] = para_email
        msg.set_content(corpo)

        # Anexo JSON
        msg.add_attachment(json.dumps(anexo_json, ensure_ascii=False, indent=4).encode("utf-8"), 
                           maintype='application', subtype='json', filename='dados_contrato.json')

        # Configurar servidor SMTP - exemplo Gmail
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_user = "seuemail@gmail.com"     # Troque pelo seu e-mail
        smtp_pass = "suasenhaaplicativo"     # Troque pela senha app (não use sua senha normal)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Erro ao enviar email:", e)
        return False

# --- Login ---
def login():
    st.title("Login - Setor de Agrupamento - Grupo Reobote Serviços")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        admins = carregar_json(ARQ_ADMINS)
        if usuario in admins and admins[usuario]["senha"] == hash_senha(senha):
            st.success(f"Bem vindo(a), {usuario}!")
            st.session_state['logado'] = True
            st.session_state['usuario'] = usuario
            st.session_state['tipo'] = admins[usuario]["tipo"]
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")

# --- Painel Admin Principal ---
def painel_admin_principal():
    st.title("Painel Administrador Principal - Grupo Reobote Serviços")

    menu = st.sidebar.selectbox("Menu", ["Administradores", "Artistas", "Visualizar Contratos", "Logout"])

    if menu == "Administradores":
        st.header("Gerenciar Administradores Comuns")
        admins = carregar_json(ARQ_ADMINS)

        st.subheader("Adicionar Administrador Comum")
        novo_admin = st.text_input("Nome do usuário")
        nova_senha = st.text_input("Senha", type="password")
        if st.button("Adicionar Administrador"):
            if novo_admin and nova_senha:
                if novo_admin in admins:
                    st.error("Usuário já existe.")
                else:
                    admins[novo_admin] = {"senha": hash_senha(nova_senha), "tipo": "comum"}
                    salvar_json(ARQ_ADMINS, admins)
                    st.success(f"Administrador {novo_admin} adicionado.")
            else:
                st.error("Preencha todos os campos.")

        st.subheader("Administradores cadastrados")
        for u, dados in admins.items():
            if dados["tipo"] == "comum":
                col1, col2 = st.columns([3,1])
                col1.write(f"Usuário: {u}")
                if col2.button(f"Deletar {u}"):
                    del admins[u]
                    salvar_json(ARQ_ADMINS, admins)
                    st.experimental_rerun()

    elif menu == "Artistas":
        st.header("Gerenciar Artistas e Serviços")
        artistas = carregar_json(ARQ_ARTISTAS)

        st.subheader("Adicionar/Editar Artista")
        nome_artista = st.text_input("Nome do Artista")
        preco_artista = st.number_input("Preço do Serviço (R$)", min_value=0.0, format="%.2f")
        if st.button("Salvar Artista"):
            if nome_artista.strip():
                artistas[nome_artista] = {"preco": preco_artista}
                salvar_json(ARQ_ARTISTAS, artistas)
                st.success(f"Artista {nome_artista} salvo.")
            else:
                st.error("Informe o nome do artista.")

        st.subheader("Artistas cadastrados")
        for nome, dados in artistas.items():
            col1, col2 = st.columns([3,1])
            col1.write(f"{nome} - R$ {dados['preco']:.2f}")
            if col2.button(f"Deletar {nome}"):
                del artistas[nome]
                salvar_json(ARQ_ARTISTAS, artistas)
                st.experimental_rerun()

    elif menu == "Visualizar Contratos":
        st.header("Contratos Recebidos")
        contratos = carregar_json(ARQ_CONTRATOS)
        if contratos:
            for cid, contrato in contratos.items():
                st.write(f"ID: {cid}")
                st.json(contrato)
                st.markdown("---")
        else:
            st.info("Nenhum contrato enviado ainda.")

    elif menu == "Logout":
        st.session_state.clear()
        st.experimental_rerun()

# --- Painel Administrador Comum ---
def painel_admin_comum():
    st.title("Painel Administrador Comum - Grupo Reobote Serviços")
    menu = st.sidebar.selectbox("Menu", ["Visualizar e Editar Contratos", "Logout"])

    if menu == "Visualizar e Editar Contratos":
        st.header("Contratos Recebidos")
        contratos = carregar_json(ARQ_CONTRATOS)
        artistas = carregar_json(ARQ_ARTISTAS)
        if contratos:
            id_contrato = st.selectbox("Selecione o ID do contrato para editar", list(contratos.keys()))
            contrato = contratos[id_contrato]
            st.write("Dados do contrato:")
            contrato['nome'] = st.text_input("Nome", contrato.get('nome', ''))
            contrato['cpf'] = st.text_input("CPF", contrato.get('cpf', ''))
            contrato['documento'] = st.text_input("Documento de Identificação", contrato.get('documento', ''))
            contrato['rua'] = st.text_input("Rua", contrato.get('rua', ''))
            contrato['bairro'] = st.text_input("Bairro", contrato.get('bairro', ''))
            contrato['cidade'] = st.text_input("Cidade", contrato.get('cidade', ''))
            contrato['numero'] = st.text_input("Número", contrato.get('numero', ''))
            contrato['email'] = st.text_input("E-mail", contrato.get('email', ''))
            contrato['telefone'] = st.text_input("Telefone", contrato.get('telefone', ''))
            contrato['tipo_contrato'] = st.selectbox("Tipo de contrato", ["Parceria", "Vínculo de assessoria", "Agendamento de artistas"], index=["Parceria", "Vínculo de assessoria", "Agendamento de artistas"].index(contrato.get('tipo_contrato','Parceria')))
            
            if st.button("Salvar
