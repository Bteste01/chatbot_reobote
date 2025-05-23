import streamlit as st

def chatbot_web():
    st.title("Chatbot Grupo Reobote Serviços")

    # Botão para iniciar o diálogo
    if 'started' not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        if st.button("Iniciar conversa"):
            st.session_state.started = True
            st.session_state.step = 1
            st.session_state.nome = ''
            st.session_state.cidade = ''
            st.session_state.estado = ''
            st.session_state.servico = ''
        else:
            st.write("Clique no botão acima para iniciar a conversa.")
        return  # Sai da função até usuário clicar no botão

    # Fluxo de perguntas do chatbot
    if 'step' not in st.session_state:
        st.session_state.step = 1
        st.session_state.nome = ''
        st.session_state.cidade = ''
        st.session_state.estado = ''
        st.session_state.servico = ''

    if st.session_state.step == 1:
        st.write("Olá! Qual o seu nome?")
        nome = st.text_input("Digite seu nome aqui", key="nome_input")
        if nome:
            st.session_state.nome = nome
            st.session_state.step = 2
            st.experimental_rerun()

    elif st.session_state.step == 2:
        st.write(f"Olá, {st.session_state.nome}! Qual a sua cidade?")
        cidade = st.text_input("Cidade", key="cidade_input")
        if cidade:
            st.session_state.cidade = cidade
            st.session_state.step = 3
            st.experimental_rerun()

    elif st.session_state.step == 3:
        st.write(f"Legal, {st.session_state.nome} de {st.session_state.cidade}! Qual o seu estado?")
        estado = st.text_input("Estado", key="estado_input")
        if estado:
            st.session_state.estado = estado
            st.session_state.step = 4
            st.experimental_rerun()

    elif st.session_state.step == 4:
        st.write(f"Ótimo, {st.session_state.nome} de {st.session_state.cidade} - {st.session_state.estado}!")
        st.write("Qual serviço você deseja?")
        servico = st.radio("Escolha uma opção:", ("Parceria", "Vínculo de assessoria", "Agendar com artista"), key="servico_input")

        if st.button("Confirmar"):
            st.session_state.servico = servico
            st.session_state.step = 5
            st.experimental_rerun()

    elif st.session_state.step == 5:
        st.write(f"Muito obrigado, {st.session_state.nome}!")
        st.write(f"Você escolheu o serviço: **{st.session_state.servico}**.")
        st.write(f"Registramos seu pedido para {st.session_state.cidade} - {st.session_state.estado}.")
        st.write("Em breve entraremos em contato pelo WhatsApp.")

if __name__ == "__main__":
    chatbot_web()
