import streamlit as st
from paginas.adm import interface_adm
from paginas.usuario import interface_usuario_comum

# Senha simples para o ADM
SENHA_ADM = "admin123"

def main():
 
    # Usando st.session_state para manter o estado de acesso do ADM
    if 'acesso_adm' not in st.session_state:
        st.session_state.acesso_adm = False

    st.sidebar.title("Navegação")

    if st.session_state.acesso_adm:
        if st.sidebar.button("Voltar para Usuário Comum"):
            st.session_state.acesso_adm = False
        interface_adm()
    else:
        senha = st.sidebar.text_input("Digite a senha ADM", type="password")
        if senha == SENHA_ADM:
            st.session_state.acesso_adm = True
        elif senha:
            st.sidebar.error("Senha incorreta.")
        interface_usuario_comum()

if __name__ == "__main__":
    main()