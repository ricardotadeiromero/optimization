import streamlit as st
from teacher_schedule import teacher_scheduler_solver

st.title("Home Page")

results = {}

if st.session_state.teachers and st.session_state.disciplines_per_teacher and st.session_state.classes and st.session_state.workload_per_discipline and st.session_state.classes_per_day:
    st.write("### Número de aulas no dia:")
    st.session_state.classes_per_day = st.number_input("Digite o numero de aulas",step=1, min_value=1)
    if st.button("Rodar Solver"):
        results = teacher_scheduler_solver(st.session_state.teachers, st.session_state.disciplines_per_teacher, st.session_state.classes, st.session_state.workload_per_discipline, st.session_state.classes_per_day)
else:
    st.write("Por favor preencha os dados primeiro.")

if results[0]:
    for c, schedule in results[0].items():
       with st.expander(f"Cronograma turma {c}"):
           st.table(schedule)

print(results)
if not results[1].empty:
    st.bar_chart(results[1])