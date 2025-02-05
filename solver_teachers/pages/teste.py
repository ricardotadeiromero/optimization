import streamlit as st

# Inicializar os estados
if "teachers" not in st.session_state:
    st.session_state.teachers = [
        "Alan", "Bignicius", "Jorge", "Camila", "Thiago", "Pedro", "Carlos", "Beatriz"
    ]

if "disciplines_per_teacher" not in st.session_state:
    st.session_state.disciplines_per_teacher = {}

if "workload" not in st.session_state:
    st.session_state.workload = {
        "Matemática": 4,
        "Português": 4,
        "Ciências": 4,
        "Artes": 2,
        "Inglês": 4,
        "Geografia": 2,
        "História": 2,
        "Educação Física": 3,
    }

# 1. Gerenciar professores
st.title("Gerenciamento de Professores e Disciplinas")

st.header("Professores")
teacher_name = st.text_input("Adicionar novo professor:")
if st.button("Adicionar Professor"):
    if teacher_name and teacher_name not in st.session_state.teachers:
        st.session_state.teachers.append(teacher_name)
        st.success(f"Professor {teacher_name} adicionado!")
    elif teacher_name in st.session_state.teachers:
        st.warning("Este professor já foi adicionado.")
    else:
        st.warning("Insira um nome válido.")

# Listar professores com opção de remoção
st.write("### Lista de Professores")
for teacher in st.session_state.teachers:
    col1, col2 = st.columns([3, 1])
    col1.write(teacher)
    if col2.button("Remover", key=f"remove_{teacher}"):
        st.session_state.teachers.remove(teacher)
        st.experimental_rerun()

# 2. Atribuir disciplinas
st.header("Atribuir Disciplinas")
selected_teacher = st.selectbox("Selecione um professor:", st.session_state.teachers)
assigned_disciplines = st.multiselect(
    "Selecione as disciplinas para este professor:",
    st.session_state.workload.keys(),
    st.session_state.disciplines_per_teacher.get(selected_teacher, []),
)

if st.button("Salvar Atribuições"):
    st.session_state.disciplines_per_teacher[selected_teacher] = assigned_disciplines
    st.success(f"Disciplinas atualizadas para {selected_teacher}!")

st.write(f"Disciplinas de {selected_teacher}: {st.session_state.disciplines_per_teacher.get(selected_teacher, [])}")

# 3. Configurar carga horária
st.header("Carga Horária por Disciplina")
for discipline, hours in st.session_state.workload.items():
    st.session_state.workload[discipline] = st.number_input(
        f"Carga horária para {discipline}:", value=hours, step=1, format="%d"
    )

st.write("### Carga Horária Atual:")
st.write(st.session_state.workload)
