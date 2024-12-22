import streamlit as st




# Adicionar ou remover professores
st.write("### Professores")
teacher_name = st.text_input("Nome do professor:")
if st.button("Adicionar Professor"):
    if teacher_name and teacher_name not in st.session_state.teachers:
        st.session_state.teachers.append(teacher_name)
        st.success(f"Professor {teacher_name} adicionado!")
    elif teacher_name in st.session_state.teachers:
        st.warning("Este professor já existe.")
    else:
        st.warning("Insira um nome válido.")

if st.session_state.teachers:
    st.write("Lista de Professores:")
    st.session_state.teachers = st.data_editor(st.session_state.teachers, num_rows="dynamic")