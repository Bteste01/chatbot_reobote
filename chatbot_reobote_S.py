import streamlit as st
import json
from datetime import date, time

def salvar_dados(dados):
    with open("contratos_dados.json", "a", encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False)
        f.write("\n")

st.set_page_config(page_title="Contratos e Ações", layout="centered")
st.title("Grupo Reobote Serviços")
st.subheader("Sistema: Contratos e Ações")

if "etapa" not in st.session_state:
    st.session_state.etapa = 1
    st.session_state.dados = {}

if st.session_state.etapa == 1:
    st.write("Informe seu nome completo:")
    nome = st.text_input("Nome")
    if st.button("Enviar nome") and nome:
        st.session_state.dados["nome"] = nome
        st.session_state.etapa = 2
        st.experimental_rerun()

elif st.session_state.etapa == 2:
    cpf = st.text_input("CPF")
    documento = st.text_input("Documento de Identificação")
    if st.button("Enviar dados de identidade") and cpf and documento:
        st.session_state.dados.update({"cpf": cpf, "documento": documento})
        st.session_state.etapa = 3
        st.experimental_rerun()

elif st.session_state.etapa == 3:
    rua = st.text_input("Rua")
    numero = st.text_input("Número")
    bairro = st.text_input("Bairro")
    cidade = st.text_input("Cidade")
    estado = st.text_input("Estado")
    if st.button("Enviar endereço") and all([rua, numero, bairro, cidade, estado]):
        st.session_state.dados.update({
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        })
        st.session_state.etapa = 4
        st.experimental_rerun()

elif st.session_state.etapa == 4:
    email = st.text_input("E-mail")
    telefone = st.text_input("Telefone")
    if st.button("Enviar contato") and email and telefone:
        st.session_state.dados.update({"email": email, "telefone": telefone})
        st.session_state.etapa = 5
        st.experimental_rerun()

elif st.session_state.etapa == 5:
    tipo = st.radio("Escolha o tipo de contrato:", ["Parceria", "Vínculo de assessoria", "Agendamento com artista"])
    if st.button("Confirmar tipo de contrato"):
        st.session_state.dados["tipo"] = tipo
        st.session_state.etapa = 6
        st.experimental_rerun()

elif st.session_state.etapa == 6:
    tipo = st.session_state.dados["tipo"]

    if tipo == "Parceria":
        clausula = "Cláusula Parceria: Ambas as partes se comprometem a cooperar sem fins lucrativos."
        st.session_state.dados["clausulas"] = clausula
        st.write(clausula)
        st.session_state.etapa = 9
        st.experimental_rerun()

    elif tipo == "Vínculo de assessoria":
        clausula = "Cláusula Assessoria: O cliente receberá suporte completo durante o período do contrato."
        st.write(clausula)
        prazo = st.selectbox("Prazo do contrato:", ["3 meses", "6 meses", "12 meses"])
        pagamento = st.selectbox("Forma de pagamento:", ["Pix", "Cartão", "Boleto"])
        if st.button("Confirmar vínculo"):
            st.session_state.dados.update({
                "clausulas": clausula,
                "prazo": prazo,
                "pagamento": pagamento
            })
            st.session_state.etapa = 9
            st.experimental_rerun()

    elif tipo == "Agendamento com artista":
        clausula = "Cláusula Agendamento: O evento será realizado conforme as informações de data e hora."
        st.write(clausula)
        data_evento = st.date_input("Data do evento", value=date.today())
        hora_inicio = st.time_input("Hora de início")
        hora_termino = st.time_input("Hora de término")
        pagamento = st.selectbox("Forma de pagamento:", ["Pix", "Cartão", "Boleto"])
        if st.button("Confirmar agendamento"):
            st.session_state.dados.update({
                "clausulas": clausula,
                "data_evento": str(data_evento),
                "hora_inicio": str(hora_inicio),
                "hora_termino": str(hora_termino),
                "pagamento": pagamento
            })
            st.session_state.etapa = 9
            st.experimental_rerun()

elif st.session_state.etapa == 9:
    st.success("Contrato preenchido com sucesso!")
    salvar_dados(st.session_state.dados)
    st.write("Resumo dos dados:")
    st.json(st.session_state.dados)
