# main.py
import streamlit as st
from paginas.adm import interface_adm
from paginas.usuario import interface_usuario_comum

# Senha simples para o ADM
SENHA_ADM = "admin123"

def main():
    st.sidebar.title("Navegação")

    if 'acesso_adm' not in st.session_state:
        st.session_state.acesso_adm = False
    
    if 'mostrar_login_adm' not in st.session_state:
        st.session_state.mostrar_login_adm = False

    if st.session_state.acesso_adm:
        if st.sidebar.button("Voltar para Usuário Comum"):
            st.session_state.acesso_adm = False
            st.session_state.mostrar_login_adm = False
        interface_adm()
    else:
        if st.sidebar.button("Acesso ADM"):
            st.session_state.mostrar_login_adm = True

        if st.session_state.mostrar_login_adm:
            senha = st.sidebar.text_input("Digite a senha ADM", type="password")
            if senha == SENHA_ADM:
                st.session_state.acesso_adm = True
                st.session_state.mostrar_login_adm = False 
            elif senha:
                st.sidebar.error("Senha incorreta.")

        interface_usuario_comum()

if __name__ == "__main__":
    main()