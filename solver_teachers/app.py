import streamlit as st
import pandas as pd

# Inicializar estado para professores e disciplinas

if "teachers" not in st.session_state:
    st.session_state.teachers = [
        "Alan", "Bignicius", "Jorge", "Camila", "Thiago", "Pedro", 
        "Carlos", "Beatriz"
    ]
if "classes" not in st.session_state:
    st.session_state.classes = []

if "disciplines_per_teacher" not in st.session_state:
    st.session_state.disciplines_per_teacher = {}

if "workload_per_discipline" not in st.session_state:
    st.session_state.workload_per_discipline = {}

pages = [
        st.Page("pages/home.py", title="Home"),
        st.Page("pages/teachers.py", title="Professores"),
        st.Page("pages/classes.py", title="Turmas"),
        st.Page("pages/disciplines.py", title="Disciplinas")
]

pg = st.navigation(pages)
pg.run()






