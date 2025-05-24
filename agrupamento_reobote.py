import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import io
import json

# Estado inicial
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []
if 'admin_principal' not in st.session_state:
    st.session_state.admin_principal = {'email': 'admin@admin.com', 'senha': 'admin'}
if 'admins' not in st.session_state:
    st.session_state.admins = []
if 'whatsapp' not in st.session_state:
    st.session_state.whatsapp = ''
if 'empresa' not in st.session_state:
    st.session_state.empresa = {'nome': 'AGRUPAMENTO REOBOTE SERVIÇOS', 'descricao': '', 'logotipo': None}
if 'artistas_disponiveis' not in st.session_state:
    st.session_state.artistas_disponiveis = []
if 'servicos_disponiveis' not in st.session_state:
    st.session_state.servicos_disponiveis = ["Agendamento com Artista", "Parceria", "Vínculo de Assessoria", "Ações no Contrato"]

# Tela Inicial - Escolha de Serviço
st.title(st.session_state.empresa['nome'])

if st.session_state.empresa['logotipo']:
    st.image(st.session_state.empresa['logotipo'], width=100)

servico_escolhido = st.selectbox("Escolha o serviço desejado", st.session_state.servicos_disponiveis)

if servico_escolhido == "Agendamento com Artista":
    st.header("Agendamento com Artista")
    if st.session_state.artistas_disponiveis:
        artista_nomes = [a['nome'] for a in st.session_state.artistas_disponiveis]
        artista_selecionado = st.selectbox("Escolha um artista", artista_nomes)
        artista_info = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista_selecionado)
        if artista_info.get('foto'):
            st.image(artista_info['foto'], width=150)
        st.write("**Descrição:**", artista_info.get('descricao', ''))
        st.write("**Categoria:**", artista_info.get('categoria', ''))

        servico_opcoes = [f"{s['nome']} - R${s['preco']:.2f}" for s in artista_info.get('servicos', [])]
        servico_escolhido = st.selectbox("Escolha o serviço", servico_opcoes)

        nome_cliente = st.text_input("Seu nome")
        email_cliente = st.text_input("Email")
        telefone_cliente = st.text_input("Telefone")
        cidade_cliente = st.text_input("Cidade")
        data_evento = st.date_input("Data do evento")
        hora_inicio = st.time_input("Hora de início")
        hora_fim = st.time_input("Hora de término")

        if st.button("Confirmar Agendamento"):
            inicio = datetime.combine(data_evento, hora_inicio)
            fim = datetime.combine(data_evento, hora_fim)
            conflito = any(
                ag['artista'] == artista_selecionado and
                not (fim <= ag['inicio'] or inicio >= ag['fim'])
                for ag in st.session_state.agendamentos
            )
            if conflito:
                st.error("Esse horário já está ocupado para este artista.")
            else:
                st.session_state.agendamentos.append({
                    'artista': artista_selecionado,
                    'servico': servico_escolhido,
                    'cliente': nome_cliente,
                    'email': email_cliente,
                    'telefone': telefone_cliente,
                    'cidade': cidade_cliente,
                    'inicio': inicio,
                    'fim': fim
                })
                st.success("Agendamento realizado com sucesso!")
    else:
        st.warning("Nenhum artista disponível.")

elif servico_escolhido == "Parceria":
    st.header("Parcerias com a Empresa")
    st.text_input("Nome da Empresa Parceira")
    st.text_input("Email para Contato")
    st.text_area("Mensagem ou Proposta")
    st.button("Enviar Proposta de Parceria")

elif servico_escolhido == "Vínculo de Assessoria":
    st.header("Quero ser Assessorado")
    st.text_input("Nome Completo")
    st.text_input("Email")
    st.text_area("Conte-nos sobre você e seu trabalho artístico")
    st.button("Enviar Solicitação de Vínculo")

elif servico_escolhido == "Ações no Contrato":
    st.header("Ações no Contrato")
    acao = st.selectbox("Escolha a ação desejada", ["Rescisão de Contrato", "Cancelar Contrato", "Meus Contratos"])

    if acao == "Rescisão de Contrato":
        tipo = st.selectbox("Tipo de Contrato", ["Parceria", "Vínculo de Assessoria"])
        st.text_input("Nome Completo")
        st.text_input("Email")
        st.text_area("Motivo da Rescisão")
        st.button("Solicitar Rescisão")

    elif acao == "Cancelar Contrato":
        st.text_input("Código do Contrato")
        st.text_input("Nome")
        st.text_input("Email")
        st.button("Solicitar Cancelamento")

    elif acao == "Meus Contratos":
        st.text_input("Digite seu email para buscar seus contratos")
        st.info("Funcionalidade em desenvolvimento")

# WhatsApp
if st.session_state.whatsapp:
    whatsapp_link = f"https://wa.me/{st.session_state.whatsapp.replace('+', '').replace(' ', '')}"
    st.markdown(f"[Fale conosco no WhatsApp]({whatsapp_link})", unsafe_allow_html=True)

# Área do Administrador
st.markdown("---")
with st.expander("Área do Administrador"):
    login_email = st.text_input("Email do administrador")
    login_senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if login_email == st.session_state.admin_principal['email'] and login_senha == st.session_state.admin_principal['senha']:
            st.session_state.admin_logado = 'principal'
            st.success("Login como administrador principal!")
        elif any(a['email'] == login_email and a['senha'] == login_senha for a in st.session_state.admins):
            st.session_state.admin_logado = login_email
            st.success("Login como administrador!")
        else:
            st.error("Credenciais inválidas.")

if st.session_state.get('admin_logado') == 'principal':
    st.header("Painel do Administrador Principal")

    st.subheader("Cadastrar Novo Administrador")
    email_novo = st.text_input("Email do novo administrador")
    senha_nova = st.text_input("Senha", type="password")
    if st.button("Cadastrar Novo Administrador"):
        if email_novo in [a['email'] for a in st.session_state.admins]:
            st.warning("Administrador já cadastrado")
        else:
            st.session_state.admins.append({"email": email_novo, "senha": senha_nova})
            st.success("Novo administrador cadastrado com sucesso")

    st.subheader("Configurações da Empresa")
    nome_empresa = st.text_input("Nome da empresa", value=st.session_state.empresa['nome'])
    descricao_empresa = st.text_area("Descrição", value=st.session_state.empresa['descricao'])
    logotipo = st.file_uploader("Logotipo", type=["png", "jpg"])
    whatsapp_numero = st.text_input("Número de WhatsApp", value=st.session_state.whatsapp)
    if st.button("Salvar Dados da Empresa"):
        st.session_state.empresa['nome'] = nome_empresa
        st.session_state.empresa['descricao'] = descricao_empresa
        if logotipo:
            st.session_state.empresa['logotipo'] = Image.open(logotipo)
        st.session_state.whatsapp = whatsapp_numero
        st.success("Dados atualizados")

    st.subheader("Gerenciar Artistas")
    nome_artista = st.text_input("Nome do artista")
    categoria = st.text_input("Categoria")
    descricao = st.text_area("Descrição")
    foto = st.file_uploader("Foto do artista")
    if st.button("Cadastrar Artista"):
        novo_artista = {
            "nome": nome_artista,
            "categoria": categoria,
            "descricao": descricao,
            "foto": Image.open(foto) if foto else None,
            "servicos": []
        }
        st.session_state.artistas_disponiveis.append(novo_artista)
        st.success("Artista cadastrado")

    if st.session_state.artistas_disponiveis:
        nomes_artistas = [a['nome'] for a in st.session_state.artistas_disponiveis]
        artista_excluir = st.selectbox("Escolha artista para excluir", nomes_artistas)
        if st.button("Excluir Artista"):
            st.session_state.artistas_disponiveis = [a for a in st.session_state.artistas_disponiveis if a['nome'] != artista_excluir]
            st.success("Artista excluído")

    st.subheader("Serviços de Artistas")
    if st.session_state.artistas_disponiveis:
        artista_servico = st.selectbox("Artista para serviços", [a['nome'] for a in st.session_state.artistas_disponiveis])
        nome_servico = st.text_input("Nome do serviço")
        preco_servico = st.number_input("Preço do serviço", min_value=0.0, step=50.0)
        if st.button("Cadastrar Serviço"):
            for artista in st.session_state.artistas_disponiveis:
                if artista['nome'] == artista_servico:
                    artista.setdefault('servicos', []).append({"nome": nome_servico, "preco": preco_servico})
                    st.success("Serviço cadastrado")

        artista_obj = next(a for a in st.session_state.artistas_disponiveis if a['nome'] == artista_servico)
        if artista_obj.get('servicos'):
            servico_excluir = st.selectbox("Serviço para excluir", [s['nome'] for s in artista_obj['servicos']])
            if st.button("Excluir Serviço"):
                artista_obj['servicos'] = [s for s in artista_obj['servicos'] if s['nome'] != servico_excluir]
                st.success("Serviço excluído")

    st.subheader("Backup e Restauração")
    if st.button("Fazer backup dos dados"):
        dados_backup = {
            "agendamentos": st.session_state.agendamentos,
            "artistas_disponiveis": st.session_state.artistas_disponiveis,
            "admins": st.session_state.admins,
            "empresa": st.session_state.empresa,
            "whatsapp": st.session_state.whatsapp
        }
        conteudo_json = json.dumps(dados_backup, default=str, indent=2)
        st.download_button("Clique para baixar o backup", conteudo_json, file_name="backup_agendamentos.json")

    arquivo_backup = st.file_uploader("Carregar backup (.json)", type=["json"])
    if arquivo_backup:
        dados = json.load(arquivo_backup)
        st.session_state.agendamentos = dados.get("agendamentos", [])
        st.session_state.artistas_disponiveis = dados.get("artistas_disponiveis", [])
        st.session_state.admins = dados.get("admins", [])
        st.session_state.empresa = dados.get("empresa", {})
        st.session_state.whatsapp = dados.get("whatsapp", "")
        st.success("Backup carregado com sucesso!")
                         
