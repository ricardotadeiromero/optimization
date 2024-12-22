import streamlit as st



# Atribuir disciplinas a professores
disciplines = [
    "Matemática", "Português", "Ciências", "Artes", 
    "Educação Física", "Inglês", "Geografia", "História"
]

if "classes_per_day" not in st.session_state:
    st.session_state.classes_per_day = 1






def reset_disciplines():
    st.session_state.assign_disciplines = []

st.write("### Atribuir Disciplinas aos Professores")
selected_teacher = st.selectbox("Selecione um professor:", st.session_state.teachers,
    on_change = reset_disciplines
                                )
assigned_disciplines = st.pills(
    "Selecione as disciplinas para este professor:", 
    disciplines, 
    selection_mode="multi",
    key="assign_disciplines",
)


# Botão para atribuir disciplinas
if st.button("Atribuir Disciplinas"):
    if selected_teacher:
        st.session_state.disciplines_per_teacher[selected_teacher] = assigned_disciplines
        print(st.session_state.disciplines_per_teacher)
        st.success(f"Disciplinas atribuídas a {selected_teacher}: {assigned_disciplines}")
    else:
        st.warning("Selecione um professor.")
# Mostrar as disciplinas atribuídas
if st.session_state.disciplines_per_teacher:
    st.write("Disciplinas por Professor:")
    st.write(st.session_state.disciplines_per_teacher)


st.write("### Carga horária de cada disciplina:")
selected_discipline = st.selectbox("Selecione uma disciplina:", disciplines,
                                )
workload = st.number_input("Digite a carga em horas",step=1, min_value=1)

if st.button("Atribuir Carga Horária"): 
    if selected_discipline:
        st.session_state.workload_per_discipline[selected_discipline] = workload
        st.success("Adicionado com sucesso!")
    else:
        st.warning("Selecione uma discipline")
# Mostrar as disciplinas atribuídas
if st.session_state.workload_per_discipline:
    st.write("Carga Horária por Disciplina:")
    st.session_state.workload_per_discipline = st.data_editor(st.session_state.workload_per_discipline,key="aa",
                                                           num_rows="dynamic")
