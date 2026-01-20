import streamlit as st
import pandas as pd
import time

# 1. Конфигурация и Стилизация
st.set_page_config(page_title="Геймърски Рай", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .main-title {
        font-size: 60px; font-weight: 800; text-align: center;
        background: -webkit-linear-gradient(#00DBDE, #FC00FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0px 10px 20px rgba(252, 0, 255, 0.3); margin-bottom: 10px;
    }
    .winner-card {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        border: 2px solid #FFD700; border-radius: 20px; padding: 30px;
        text-align: center; box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.2);
        margin-bottom: 40px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00DBDE 0%, #FC00FF 100%);
        color: white; border: none; padding: 15px 30px; font-size: 20px;
        font-weight: bold; border-radius: 50px; transition: 0.3s;
        box-shadow: 0px 5px 15px rgba(252, 0, 255, 0.4);
    }
    .stButton>button:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- Инициализация на данни ---
if "game_votes" not in st.session_state:
    st.session_state.game_votes = {
        "Minecraft ⛏️": 0, "Roblox 🤖": 0, "Brawl Stars ⭐": 0,
        "Fortnite 🔫": 0, "CS:GO / CS2 💣": 0, "FIFA / FC24 ⚽": 0,
        "League of Legends 🏆": 0
    }

# --- ГЛАВЕН ПАНЕЛ ---
st.markdown('<p class="main-title">LEVEL UP: КЛАСНА АНКЕТА</p>', unsafe_allow_html=True)

# Изчисляване на гласовете
total_votes = sum(st.session_state.game_votes.values())
# Взимаме само игрите, които имат поне 1 глас
games_with_votes = {name: v for name, v in st.session_state.game_votes.items() if v > 0}

# --- ПОБЕДИТЕЛ (Показва се само при наличие на гласове) ---
if total_votes > 0:
    popular_game = max(st.session_state.game_votes, key=st.session_state.game_votes.get)
    col_space1, col_winner, col_space2 = st.columns([1, 2, 1])
    with col_winner:
        st.markdown(f"""
        <div class="winner-card">
            <h2 style="color: #FFD700; margin-top: 0;">👑 ЛИДЕР В КЛАСАЦИЯТА 👑</h2>
            <h1 style="font-size: 50px; margin: 10px 0;">{popular_game}</h1>
            <p style="font-size: 20px; opacity: 0.8;">Води с {st.session_state.game_votes[popular_game]} гласа!</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("🎮 Все още няма гласували. Бъди първи!")

# --- СЕКЦИЯ ЗА ГЛАСУВАНЕ ---
st.divider()
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown("### 🗳️ Гласувай за игра")
    choice = st.radio("Избери фаворит:", list(st.session_state.game_votes.keys()))
    if st.button("ИЗПРАТИ ГЛАС 🚀"):
        st.session_state.game_votes[choice] += 1
        st.balloons()
        time.sleep(0.5)
        st.rerun()

with c2:
    st.markdown("### 📊 Всички резултати")
    df = pd.DataFrame.from_dict(st.session_state.game_votes, orient="index", columns=["Гласове"])
    st.bar_chart(df, color="#FC00FF")

# --- ЛОГИКА ЗА ТОП 3 (Показва се само ако има игри с гласове) ---
if games_with_votes:
    st.divider()
    st.markdown("### 🏆 Текуща Топ Класация")
    
    # Сортираме и взимаме само първите 3, които имат гласове
    top_3 = sorted(games_with_votes.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Правим толкова колони, колкото игри има в Топ 3 (може да е 1, 2 или 3)
    cols = st.columns(len(top_3))
    
    for i, (name, votes) in enumerate(top_3):
        with cols[i]:
            st.metric(label=f"Място #{i+1}", value=name, delta=f"{votes} гласа")

# Странично меню
with st.sidebar:
    st.title("🕹️ Опции")
    if st.button("🗑️ Нулирай всички гласове"):
        for k in st.session_state.game_votes: st.session_state.game_votes[k] = 0
        st.rerun()
