import streamlit as st
import uuid
from ..dados import carregar_dados, salvar_dados, ARQUIVO_SUGESTOES

def interface_adm():
 
    st.title("🛡️ Painel ADM")

    # --- Adicionar Sugestão de Aposta ---
    st.subheader("Adicionar Nova Sugestão de Aposta")

    with st.form("form_adicionar_aposta"):
        jogo = st.text_input("Jogo (ex: vasco x flamengo)")
        tipo_aposta = st.text_input("Tipo de Aposta (ex: mais de 1,5 gols)")
        odd = st.number_input("Odd (ex: 1.5)", min_value=1.0, format="%f")
        casa_aposta = st.text_input("Casa de Aposta (ex: betano)")
        submit_button = st.form_submit_button("Adicionar Aposta")

        if submit_button:
            if jogo and tipo_aposta and odd and casa_aposta:
                id_aposta = str(uuid.uuid4())[:8]
                nova_aposta = {
                    "id": id_aposta,
                    "jogo": jogo,
                    "tipo_aposta": tipo_aposta,
                    "odd": odd,
                    "casa_aposta": casa_aposta,
                    "status": "Pendente"
                }
                sugestoes = carregar_dados(ARQUIVO_SUGESTOES)
                sugestoes.append(nova_aposta)
                salvar_dados(ARQUIVO_SUGESTOES, sugestoes)
                st.success("Sugestão de aposta adicionada com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

    # --- Validar Resultados de Apostas ---
    st.subheader("Validar Resultados de Apostas")
    sugestoes = carregar_dados(ARQUIVO_SUGESTOES)
    apostas_pendentes = [a for a in sugestoes if a.get('status') == 'Pendente']

    if apostas_pendentes:
        for aposta in apostas_pendentes:
            st.markdown("---")
            st.write(f"**Jogo:** {aposta['jogo']}")
            st.write(f"**Tipo:** {aposta['tipo_aposta']}")
            st.write(f"**Odd:** {aposta['odd']}")
            st.write(f"**ID da Aposta:** {aposta['id']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔴 RED", key=f"red_{aposta['id']}"):
                    for s in sugestoes:
                        if s.get('id') == aposta['id']:
                            s['status'] = "RED"
                    salvar_dados(ARQUIVO_SUGESTOES, sugestoes)
                    st.success(f"Resultado da aposta '{aposta['jogo']}' atualizado para RED.")
                    
            with col2:
                if st.button("🟢 GREEN", key=f"green_{aposta['id']}"):
                    for s in sugestoes:
                        if s.get('id') == aposta['id']:
                            s['status'] = "GREEN"
                    salvar_dados(ARQUIVO_SUGESTOES, sugestoes)
                    st.success(f"Resultado da aposta '{aposta['jogo']}' atualizado para GREEN.")
                    
    else:
        st.info("Não há apostas pendentes para validar.")
