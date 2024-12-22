from pulp import *
import pandas as pd
from openpyxl import Workbook

# Dados do problema
teachers = [
    "Alan", "Bignicius", "Jorge", "Camila", "Thiago", "Pedro", 
     "Carlos", "Beatriz"
]
classes = ["A", "B", "C", "D", "E"]
disciplines = ["Matemática", "Português", "Ciências", "Artes", "Educação Física", "Inglês", "Geografia", "História"]


disciplines_per_teacher = {
    "Alan": ["Matemática", "Português"],
    "Bignicius": ["Matemática", "Ciências"],
    "Jorge": ["Artes", "Geografia", "Português"],
    "Camila": ["Português", "Artes"],
    "Thiago": ["Ciências", "Matemática"],
    "Pedro": ["Português", "História"],
    "Carlos": ["Artes", "Educação Física"],
    "Beatriz": ["Matemática", "Inglês"]
}

workload = {
    "Matemática": 4,
    "Português": 4,
    "Ciências": 4,
    "Artes": 2,
    "Inglês": 4,
    "Geografia": 2,
    "História": 2,
    "Educação Física": 3,
}


# Variável responsável por fazer a alocação
def teacher_scheduler_solver(teachers, disciplines_per_teacher, classes, workload, classes_per_day):
    slots = [f"{day}_{slot}" for day in ["Seg", "Ter", "Qua", "Qui", "Sex"] for slot in range(1, classes_per_day + 1)]  # 5 slots por dia

    workload_limit = 40

    # Mapear slots por dia para facilitar o cálculo de consecutividade
    days = ["Seg", "Ter", "Qua", "Qui", "Sex"]
    slots_per_day = {
        day: [slot for slot in slots if slot.startswith(day)] for day in days
    }
    x = LpVariable.dicts(
    "Allocation", 
    ((t, d, c, s) for t in teachers for d in disciplines_per_teacher[t] for c in classes for s in slots),
    0, 1, cat=LpBinary
    )

    # Variável de referência
    y = LpVariable.dicts(
        "Reference", 
        ((t, c, d) for t in teachers for c in classes for d in disciplines_per_teacher[t]), 
        0, 1, cat=LpBinary
    )

    prob = LpProblem("Teachers_Allocation", LpMinimize)

    # Função Objetivo (neutra, pois estamos apenas focando em satisfazer as restrições)
    prob += lpSum(x[(t, d, c, s)] * workload[d] for t in teachers for c in classes for d in disciplines_per_teacher[t] for s in slots)

    # Restrições

    # 1ª Restrição: Cumprir a carga horária
    for c in classes:
        for d in disciplines:
            prob += lpSum(
                x[(t, d, c, s)]
                for t in teachers
                if d in disciplines_per_teacher[t]  # Apenas disciplinas válidas
                for s in slots
            ) == workload[d]

    # 2ª Restrição: Apenas uma aula por horário por turma
    for c in classes: 
        for s in slots: 
            prob += lpSum(x[(t, d, c, s)] for t in teachers for d in disciplines_per_teacher[t]) <= 1

    #3ª Restrição: Apenas um professor por matéria em cada turma
    for t in teachers:
        for c in classes:
            for d in disciplines_per_teacher[t]:
                prob += lpSum(x[(t, d, c, s)] for s in slots) <= y[(t, c, d)] * workload[d]

    for c in classes:
        for d in disciplines:
            prob += lpSum(y[(t, c, d)] for t in teachers if d in disciplines_per_teacher[t]) == 1

    # 4ª Restrição: Duas aulas consecutivas da mesma disciplina na mesma turma não podem ocorrer
    for c in classes:
        for day, day_slots in slots_per_day.items():
            for i in range(len(day_slots) - 1):  # Percorrer slots consecutivos
                slot_current = day_slots[i]
                slot_next = day_slots[i + 1]
                for d in disciplines:
                    prob += lpSum(
                        x[(t, d, c, slot_current)] + x[(t, d, c, slot_next)]
                        for t in teachers if d in disciplines_per_teacher[t]
                    ) <= 1
    # 5ª Restrição: Os professores não devem exceder o limte de carga horária:
    for t in teachers:
        prob += lpSum(x[(t, d, c, s)] for c in classes for d in disciplines_per_teacher[t] for s in slots) <= workload_limit

    # Resolver o problema
    prob.solve()

    # Após resolver o problema e verificar se é viável
    if prob.status == LpStatusOptimal:
        # Inicializar um dicionário para armazenar os resultados organizados por turma
        turma_schedules = {c: pd.DataFrame(index=["Slot 1", "Slot 2", "Slot 3", "Slot 4", "Slot 5"], 
                                        columns=["Seg", "Ter", "Qua", "Qui", "Sex"])
                        for c in classes}
        workload_per_teacher = pd.DataFrame(columns=[f"{t}" for t in teachers])

        # Preencher os horários de cada turma
        for t in teachers:
            for d in disciplines_per_teacher[t]:
                for c in classes:
                    for s in slots:
                        if x[(t, d, c, s)].value() == 1:
                            day, slot_number = s.split("_")
                            slot_label = f"Slot {slot_number}"
                            turma_schedules[c].at[slot_label, day] = f"{t} ({d})"
            workload_per_teacher.at[t, "Ocupação"] = sum(
            x[(t, d, c, s)].value()
            for d in disciplines_per_teacher[t]
            for c in classes
            for s in slots
            if x[(t, d, c, s)].value() == 1  # Verifica se o professor está alocado para aquele horário
        )

        # Criar um arquivo Excel com uma aba para cada turma
        with pd.ExcelWriter("alocacao_turmas.xlsx", engine="openpyxl", mode="w") as writer:
            for c, schedule in turma_schedules.items():
                schedule.to_excel(writer, sheet_name=f"Turma {c}")
            workload_per_teacher.to_excel(writer, sheet_name=f"Workload_Teachers")
        print("Resultados salvos no arquivo 'alocacao_turmas.xlsx'.")
        return [turma_schedules,workload_per_teacher]
    else:
        print("Não foi possível encontrar uma solução viável.")

