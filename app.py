import streamlit as st
import pandas as pd
import time

# Конфигурация на страницата
st.set_page_config(page_title="Класна Анкета", page_icon="🏆", layout="centered")

# Стилизиране с малко CSS за по-готини заглавия
st.markdown("""
    <style>
    .main-title { font-size: 50px; font-weight: bold; color: #FF4B4B; text-align: center; }
    .subtitle { font-size: 20px; text-align: center; color: #555; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🏆 Великата Класна Анкета</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Гласувай за своите фаворити и виж кой води класацията!</p>', unsafe_allow_html=True)

# --- Инициализация на данните (с по-смислени имена) ---
if "people_votes" not in st.session_state:
    st.session_state.people_votes = {"Адриан": 0, "Сашо": 0, "Ачо": 0, "Синан": 0, "Берко": 0}

if "grade_votes" not in st.session_state:
    st.session_state.grade_votes = {"Шестица": 0, "Петица": 0, "Четворка": 0, "Тройка": 0, "Двойка": 0}

# --- Странично меню (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Опции")
    if st.button("🔄 Нулирай резултатите"):
        for key in st.session_state.people_votes: st.session_state.people_votes[key] = 0
        for key in st.session_state.grade_votes: st.session_state.grade_votes[key] = 0
        st.rerun()
    st.info("Тази анкета е анонимна. Гласувай смело!")

# --- Секция за гласуване ---
st.subheader("🗳️ Дай своя глас")
col1, col2 = st.columns(2)

with col1:
    person = st.radio("👤 Избери човек на деня:", list(st.session_state.people_votes.keys()))

with col2:
    grade = st.selectbox("📚 Коя оценка ти е на сърце?", list(st.session_state.grade_votes.keys()))

if st.button("🚀 ИЗПРАТИ ГЛАСА СИ"):
    # Анимация за зареждане
    with st.spinner('Обработваме твоя глас...'):
        time.sleep(0.5)
        st.session_state.people_votes[person] += 1
        st.session_state.grade_votes[grade] += 1
    
    # Визуални ефекти
    st.balloons()
    if grade == "Шестица":
        st.snow() # Сняг за отличниците!
        st.success(f"Браво! Ти подкрепи {person} и избра най-добрата оценка!")
    else:
        st.success(f"Твоят глас за {person} беше записан успешно!")

st.divider()

# --- Секция с резултати ---
st.subheader("📊 Резултати в реално време")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.write("**👑 Популярност (Хора)**")
    df_people = pd.DataFrame.from_dict(st.session_state.people_votes, orient="index", columns=["Гласове"])
    st.bar_chart(df_people, color="#FF4B4B")

with res_col2:
    st.write("**📝 Желани оценки**")
    df_grades = pd.DataFrame.from_dict(st.session_state.grade_votes, orient="index", columns=["Гласове"])
    st.line_chart(df_grades, color="#29B5E8") # Различен тип графика за разнообразие

# Показване на "Лидер" в момента
leader = max(st.session_state.people_votes, key=st.session_state.people_votes.get)
if st.session_state.people_votes[leader] > 0:
    st.info(f"🔥 В момента лидер на класа е **{leader}**!")
