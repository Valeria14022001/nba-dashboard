import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("nba_all_elo.csv")

# Convertir fecha
df["date_game"] = pd.to_datetime(df["date_game"])

# Sidebar
st.sidebar.title("Filtros")

# Selector de año
years = sorted(df["year_id"].unique())
selected_year = st.sidebar.selectbox("Selecciona un año", years)

# Filtrar por año
df_year = df[df["year_id"] == selected_year]

# Selector de equipo
teams = sorted(df_year["fran_id"].unique())
selected_team = st.sidebar.selectbox("Selecciona un equipo", teams)

# Selector tipo de juego
game_type = st.sidebar.radio(
    "Tipo de juego",
    ["Regular", "Playoffs", "Ambos"]
)

# Filtrado final
df_team = df_year[df_year["fran_id"] == selected_team]

if game_type == "Regular":
    df_team = df_team[df_team["is_playoffs"] == 0]
elif game_type == "Playoffs":
    df_team = df_team[df_team["is_playoffs"] == 1]

# Ordenar por fecha
df_team = df_team.sort_values(by="date_game")

# Calcular acumulados
df_team["wins"] = (df_team["game_result"] == "W").astype(int)
df_team["losses"] = (df_team["game_result"] == "L").astype(int)

df_team["cum_wins"] = df_team["wins"].cumsum()
df_team["cum_losses"] = df_team["losses"].cumsum()

# Dashboard
st.title("Dashboard NBA")

st.subheader("Victorias vs Derrotas acumuladas")

fig, ax = plt.subplots()

ax.plot(df_team["cum_wins"], label="Victorias")
ax.plot(df_team["cum_losses"], label="Derrotas")

ax.set_xlabel("Número de juegos")
ax.set_ylabel("Acumulado")
ax.legend()

st.pyplot(fig)

# Gráfica de pastel
st.subheader("Porcentaje de resultados")

total_wins = df_team["wins"].sum()
total_losses = df_team["losses"].sum()

fig2, ax2 = plt.subplots()

ax2.pie(
    [total_wins, total_losses],
    labels=["Victorias", "Derrotas"],
    autopct="%1.1f%%"
)

st.pyplot(fig2)