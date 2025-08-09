import streamlit as st
from datetime import datetime
from ..dados import carregar_dados, salvar_dados, ARQUIVO_SUGESTOES, ARQUIVO_USUARIOS

def interface_usuario_comum():
 
    st.title("⚽ Apostas do Dia")

    usuario_atual = st.text_input("Digite seu nome de usuário para começar:", key="nome_usuario")

    if not usuario_atual:
        st.info("Por favor, digite seu nome de usuário.")
        return

    st.subheader(f"Olá, {usuario_atual}!")

    # --- Seção de Sugestões de Aposta ---
    st.markdown("### Sugestões de Aposta Disponíveis")

    sugestoes = carregar_dados(ARQUIVO_SUGESTOES)
    apostas_usuarios = carregar_dados(ARQUIVO_USUARIOS)
    apostas_abertas = [a for a in sugestoes if a.get('status') == 'Pendente']

    if apostas_abertas:
        for aposta in apostas_abertas:
            st.markdown(f"""
            <div style="background-color:#000000; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <h4>{aposta['jogo']}</h4>
                <p><strong>Tipo de Aposta:</strong> {aposta['tipo_aposta']}</p>
                <p><strong>Odd:</strong> {aposta['odd']} | <strong>Casa:</strong> {aposta['casa_aposta']}</p>
            </div>
            """, unsafe_allow_html=True)

            ja_apostou = any(
                item['usuario'] == usuario_atual and item['id_aposta'] == aposta['id']
                for item in apostas_usuarios
            )

            if ja_apostou:
                st.info("Você já seguiu esta aposta.")
            else:
                if st.button("Apostar", key=f"apostar_{aposta['id']}"):
                    nova_aposta_usuario = {
                        "usuario": usuario_atual,
                        "id_aposta": aposta['id'],
                        "data_aposta": datetime.now().strftime("%Y-%m-%d")
                    }
                    apostas_usuarios.append(nova_aposta_usuario)
                    salvar_dados(ARQUIVO_USUARIOS, apostas_usuarios)
                    st.success("Aposta adicionada ao seu histórico!")
                    
    else:
        st.info("Nenhuma sugestão de aposta disponível no momento.")

    # --- Seção de Histórico de Apostas do Usuário ---
    st.markdown("---")
    st.markdown("### Seu Histórico de Apostas")

    historico_pessoal = [
        aposta for aposta in apostas_usuarios if aposta.get('usuario') == usuario_atual
    ]
    sugestoes_dict = {s['id']: s for s in sugestoes}

    if historico_pessoal:
        for aposta_feita in historico_pessoal:
            aposta_sugerida = sugestoes_dict.get(aposta_feita['id_aposta'])

            if aposta_sugerida:
                status = aposta_sugerida.get('status', 'Pendente')

                badge_color = "gray"
                badge_text = "Pendente"
                if status == "GREEN":
                    badge_color = "green"
                    badge_text = "GREEN"
                elif status == "RED":
                    badge_color = "red"
                    badge_text = "RED"

                st.markdown(f"""
                <div style="background-color:#000000; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <h4>{aposta_sugerida['jogo']}</h4>
                    <p><strong>Tipo de Aposta:</strong> {aposta_sugerida['tipo_aposta']}</p>
                    <p><strong>Odd:</strong> {aposta_sugerida['odd']}</p>
                    <p><strong>Data da Aposta:</strong> {aposta_feita['data_aposta']}</p>
                    <span style="background-color:{badge_color}; color:white; padding: 5px; border-radius: 5px;">{badge_text}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Você ainda não seguiu nenhuma aposta.")
