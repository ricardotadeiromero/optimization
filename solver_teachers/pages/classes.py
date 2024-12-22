import streamlit as st



st.write("### Classes")
class_name = st.text_input("Nome da turma:")
if st.button("Adicionar Turma"):
    if class_name and class_name not in st.session_state.classes:
        st.session_state.classes.append(class_name)
        st.success(f"Turma {class_name} adicionado!")
    elif class_name in st.session_state.classes:
        st.warning("Esta turma já existe.")
    else:
        st.warning("Insira uma turma válida.")


if st.session_state.classes:
    st.write("Lista de Turmas:")
    st.session_state.classes = st.data_editor(st.session_state.classes, key="bb", num_rows="dynamic")
