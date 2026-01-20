import streamlit as st
import pandas as pd
import time

# 1. Конфигурация и Стилизация
st.set_page_config(page_title="Геймърски Рай", page_icon="🎮", layout="wide")

# Декорация с CSS (Неонов стил)
st.markdown("""
    <style>
    /* Основен фон и шрифтове */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Заглавие */
    .main-title {
        font-size: 60px;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#00DBDE, #FC00FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 10px 20px rgba(252, 0, 255, 0.3);
        margin-bottom: 10px;
    }

    /* Карта за Победителя */
    .winner-card {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        border: 2px solid #FFD700;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.2);
        margin-bottom: 40px;
    }

    /* Бутони */
    .stButton>button {
        background: linear-gradient(45deg, #00DBDE 0%, #FC00FF 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        transition: 0.3s;
        box-shadow: 0px 5px 15px rgba(252, 0, 255, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 25px rgba(0, 219, 222, 0.6);
    }

    /* Контейнери за графиките */
    .plot-container {
        border-radius: 15px;
        background-color: #161b22;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Инициализация на данни ---
if "game_votes" not in st.session_state:
    st.session_state.game_votes = {
        "Minecraft ⛏️": 0,
        "Roblox 🤖": 0,
        "Brawl Stars ⭐": 0,
        "Fortnite 🔫": 0,
        "CS:GO / CS2 💣": 0,
        "FIFA / FC24 ⚽": 0,
        "League of Legends 🏆": 0
    }

# --- ГЛАВЕН ПАНЕЛ ---
st.markdown('<p class="main-title">LEVEL UP: КЛАСНА АНКЕТА</p>', unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Коя игра владее класа в момента?</p>", unsafe_allow_html=True)

# Изчисляване на победител
popular_game = max(st.session_state.game_votes, key=st.session_state.game_votes.get)
total_votes = sum(st.session_state.game_votes.values())

# --- ХОЛ НА СЛАВАТА (Winner Section) ---
col_space1, col_winner, col_space2 = st.columns([1, 2, 1])

with col_winner:
    if total_votes > 0:
        st.markdown(f"""
        <div class="winner-card">
            <h2 style="color: #FFD700; margin-top: 0;">👑 НАЙ-ПОПУЛЯРНА ИГРА 👑</h2>
            <h1 style="font-size: 50px; margin: 10px 0;">{popular_game}</h1>
            <p style="font-size: 20px; opacity: 0.8;">Води класацията с {st.session_state.game_votes[popular_game]} гласа!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("🎮 Очакваме първия глас, за да коронясаме победител!")

# --- СЕКЦИЯ ЗА ГЛАСУВАНЕ ---
st.divider()
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown("### 🗳️ Дай своя глас")
    choice = st.radio("Избери своята любима игра:", list(st.session_state.game_votes.keys()))
    
    if st.button("ИЗПРАТИ ГЛАС 🚀"):
        with st.spinner('Зареждане на данни...'):
            time.sleep(0.6)
            st.session_state.game_votes[choice] += 1
            st.balloons()
            st.rerun()

with c2:
    st.markdown("### 📊 Статистика")
    # Подготовка на данните за графиката
    df = pd.DataFrame.from_dict(st.session_state.game_votes, orient="index", columns=["Гласове"])
    df = df.sort_values(by="Гласове", ascending=True) # За да е най-отгоре най-популярната
    
    # Модерна хоризонтална графика
    st.bar_chart(df, color="#FC00FF")

# --- ДОПЪЛНИТЕЛНА ДЕКОРАЦИЯ ОТДОЛУ ---
st.divider()
st.markdown("### 🏆 Топ 3 Класация")
top_3 = sorted(st.session_state.game_votes.items(), key=lambda x: x[1], reverse=True)[:3]

cols = st.columns(3)
for i, (name, votes) in enumerate(top_3):
    with cols[i]:
        st.metric(label=f"Място #{i+1}", value=name, delta=f"{votes} гласа")

# Странично меню
with st.sidebar:
    st.title("🕹️ Меню")
    st.write("Добре дошли в официалната геймърска класация на нашия клас!")
    if st.button("🗑️ Нулирай всичко"):
        for k in st.session_state.game_votes: st.session_state.game_votes[k] = 0
        st.rerun()
    st.write("---")
    st.markdown("**Powered by Streamlit Magic ✨**")
