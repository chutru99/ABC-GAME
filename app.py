import streamlit as st
import time
from PIL import Image
from modes import mode_individual, mode_multiplayer   # ✅ incluye ambos modos

# ==============================
# 🎮 ABC GAME - Versión en español
# ==============================

st.set_page_config(
    page_title="ABC GAME",
    page_icon="resources/logo.png",  # 🟢 Logo verde como icono de la app
    layout="centered"
)

# ==============================
# 1️⃣ Estado inicial de la aplicación
# ==============================
if "screen" not in st.session_state:
    st.session_state.screen = "loading"
if "game_mode" not in st.session_state:
    st.session_state.game_mode = None


# ==============================
# 2️⃣ Funciones auxiliares
# ==============================
def go_to(screen_name: str):
    """Cambia de pantalla y recarga la app."""
    st.session_state.screen = screen_name
    st.rerun()


def show_logo(size: int = 150):
    """Muestra el logo verde si existe."""
    try:
        logo = Image.open("resources/logo.png")
        st.image(logo, use_container_width=False, width=size)
    except Exception:
        st.write("ABC GAME")


# ==============================
# 3️⃣ Pantalla de carga (Splash)
# ==============================
if st.session_state.screen == "loading":
    st.markdown(
        """
        <style>
        .centered {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 90vh;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='centered'>", unsafe_allow_html=True)
    show_logo(200)
    st.markdown("<h2>ABC GAME</h2>", unsafe_allow_html=True)
    st.markdown("<p>Cargando...</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(2)
    go_to("start")


# ==============================
# 4️⃣ Pantalla de inicio
# ==============================
elif st.session_state.screen == "start":
    show_logo(130)
    st.title("ABC GAME")
    st.subheader("El reto de las palabras con las letras de las matrículas 🚗")
    st.write("Selecciona cómo quieres jugar 👇")

    if st.button("▶️ Empezar juego"):
        go_to("select_mode")


# ==============================
# 5️⃣ Selección de modo de juego (solo individual o multijugador)
# ==============================
elif st.session_state.screen == "select_mode":
    show_logo(100)
    st.title("Selecciona el modo de juego")
    st.write("Elige si quieres jugar **solo** o **con amigos**:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧍 Modo individual"):
            st.session_state.game_mode = "individual"
            go_to("instructions")
    with col2:
        if st.button("👥 Multijugador"):
            st.session_state.game_mode = "multiplayer"
            go_to("instructions")

    if st.button("⬅️ Volver al inicio"):
        go_to("start")


# ==============================
# 6️⃣ Instrucciones (ajustadas por modo)
# ==============================
elif st.session_state.screen == "instructions":
    st.title("📘 Instrucciones del juego")

    mode = st.session_state.game_mode

    # ==============================
    # 🧍 MODO INDIVIDUAL
    # ==============================
    if mode == "individual":
        st.header("🧍 Modo individual")

        st.markdown("""
        Juegas tú solo contra el **tiempo** ⏱️.  
        El sistema te dará **tres letras aleatorias** (por ejemplo `A`, `C`, `S`), y tu objetivo es escribir
        tantas palabras válidas como puedas antes de que acabe el minuto.

        - **Tiempo por ronda:** 1 minuto.  
        - Si no escribes ninguna palabra antes de que acabe el tiempo, **termina la partida**.  
        - Cada palabra correcta suma tantos puntos como letras tenga.  
        - En este modo **no importa el orden** de las letras:  
          `A`, `C`, `S` → *CASA*, *SACO*, *ACOSO*.
        - Las palabras no pueden repetirse.
        """)

    # ==============================
    # 👥 MODO MULTIJUGADOR
    # ==============================
    else:
        st.header("👥 Modo multijugador")

        st.markdown("""
        ### 🚗 Objetivo del juego  
        Con las **tres letras** de una matrícula (por ejemplo, `C S A`), los jugadores deben proponer palabras
        del diccionario español que **contengan esas letras**.  
        Ejemplo: para `C S A`, palabras válidas serían **CASA**, **COSTA** o **CASO**.

        ### 🕹️ Dinámica
        1. Introduce las tres letras de la matrícula.  
        2. Cada jugador, por turnos, escribe una palabra y selecciona su nombre.  
        3. Si la palabra es válida y existe en el diccionario → gana **1 punto**.  
        4. Una palabra solo se puede usar **una vez** durante toda la partida.

        ### 🔁 Fin del juego
        Puedes reiniciar en cualquier momento para volver al inicio y crear una nueva partida.
        """)

    st.divider()

    # ✅ Redirige directamente al modo correspondiente
    if st.button("🚀 Empezar partida", key="launch_game"):
        if mode == "individual":
            st.session_state.screen = "game_individual"
            st.rerun()
        elif mode == "multiplayer":
            st.session_state.screen = "game_multiplayer"
            st.rerun()


# ==============================
# 7️⃣ Ejecución de los modos
# ==============================
elif st.session_state.screen == "game_individual":
    mode_individual.run_mode()

elif st.session_state.screen == "game_multiplayer":
    mode_multiplayer.run_mode()
