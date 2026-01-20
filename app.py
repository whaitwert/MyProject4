import streamlit as st
import pandas as pd
import time

# Конфигурация на страницата
st.set_page_config(page_title="Геймърска Анкета", page_icon="🎮", layout="centered")

# Стилизиране
st.markdown("""
    <style>
    .main-title { font-size: 45px; font-weight: bold; color: #7D3CFF; text-align: center; }
    .leader-box { 
        background-color: #f0f2f6; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 10px solid #FFD700;
        text-align: center;
        margin-bottom: 25px;
    }
    .game-name { color: #7D3CFF; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🎮 Коя е най-добрата видео игра?</p>', unsafe_allow_html=True)

# --- Инициализация на игрите ---
if "game_votes" not in st.session_state:
    # Можеш да добавяш или махаш игри от този списък:
    st.session_state.game_votes = {
        "Minecraft": 0,
        "Roblox": 0,
        "Brawl Stars": 0,
        "Fortnite": 0,
        "CS:GO / CS2": 0,
        "League of Legends": 0,
        "FIFA / FC24": 0,
        "GTA V": 0
    }

# --- Логика за Популярност ---
# Намираме играта с най-много гласове
popular_game = max(st.session_state.game_votes, key=st.session_state.game_votes.get)
max_votes = st.session_state.game_votes[popular_game]

# Показваме Лидера най-отгоре, ако има поне един глас
if max_votes > 0:
    st.markdown(f"""
    <div class="leader-box">
        <p style="font-size: 18px; margin-bottom: 5px;">🔥 В МОМЕНТА НАЙ-ПОПУЛЯРНА Е:</p>
        <p class="game-name">🏆 {popular_game} 🏆</p>
        <p style="color: #555;">със събрани {max_votes} гласа</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("🎯 Бъди първият, който ще гласува за своята любима игра!")

# --- Секция за гласуване ---
st.subheader("🕹️ Избери своя фаворит:")
selected_game = st.selectbox("Избери игра от списъка:", list(st.session_state.game_votes.keys()))

if st.button("🚀 ГЛАСУВАЙ СЕГА"):
    with st.spinner('Записваме твоя геймърски глас...'):
        time.sleep(0.5)
        st.session_state.game_votes[selected_game] += 1
    
    st.balloons()
    st.success(f"Ти гласува за {selected_game}! Виж как се промени класацията отдолу.")

st.divider()

# --- Резултати и Графика ---
st.subheader("📊 Текуща класация на популярността")

# Подготовка на данните за графиката
df_games = pd.DataFrame.from_dict(
    st.session_state.game_votes, 
    orient="index", 
    columns=["Гласове"]
).sort_values(by="Гласове", ascending=False) # Сортираме ги по популярност

# Показване на графиката
st.bar_chart(df_games, color="#7D3CFF")

# Странично меню за нулиране
with st.sidebar:
    st.header("Настройки")
    if st.button("🔄 Нулирай класацията"):
        for game in st.session_state.game_votes:
            st.session_state.game_votes[game] = 0
        st.rerun()
    st.write("Тази анкета показва коя игра е най-играна в момента.")
