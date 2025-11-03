import streamlit as st
import random
import time
from utils.dictionary import load_words


# ==============================
# 🧍 Modo Individual - Fácil
# ==============================
def run_mode():
    """Ejecuta el modo individual fácil."""

    words = load_words()

    # ==============================
    # 1️⃣ Estado inicial
    # ==============================
    defaults = {
        "letters": "",
        "found_words": set(),
        "score": 0,
        "total_score": 0,
        "start_time": None,
        "time_left": 60,
        "game_active": False,
        "round_finished": False,
        "word_checked": False,
        "current_word": "",
        "last_message": "",  # 💬 Mensaje temporal que se mostrará abajo
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ==============================
    # 2️⃣ Funciones internas
    # ==============================
    def choose_letters():
        """Elige tres letras distintas con ≥100 palabras posibles."""
        all_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for _ in range(3000):
            combo = "".join(random.sample(all_letters, 3))
            count = sum(1 for w in words if all(l.lower() in w for l in combo.lower()))
            if count >= 100:
                return combo
        return "CAS"

    def full_clean_for_new_round():
        """Reinicia la ronda manteniendo la puntuación total."""
        st.session_state.found_words = set()
        st.session_state.score = 0
        st.session_state.round_finished = False
        st.session_state.word_checked = False
        st.session_state.current_word = ""
        st.session_state.game_active = True
        st.session_state.start_time = time.time()
        st.session_state.time_left = 60
        st.session_state.letters = choose_letters()  # 👈 nuevas letras para la nueva ronda
        st.rerun()

    def start_game(reset_score=False):
        """Inicia nueva partida o ronda."""
        if reset_score:
            st.session_state.total_score = 0
        st.session_state.letters = choose_letters()
        st.session_state.found_words = set()
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.time_left = 60
        st.session_state.game_active = True
        st.session_state.round_finished = False
        st.session_state.word_checked = False
        st.session_state.current_word = ""

    def check_word():
        """Valida la palabra introducida."""
        if st.session_state.word_checked:
            return
        st.session_state.word_checked = True

        word = st.session_state.current_word.strip().lower()
        if not word or not st.session_state.game_active:
            st.session_state.word_checked = False
            return

        letters = st.session_state.letters.lower()
        if word in st.session_state.found_words:
            st.session_state.last_message = f"⚠️ '{word}' ya fue usada."
        elif word in words and all(l in word for l in letters):
            points = len(word)
            st.session_state.score += points
            st.session_state.total_score += points
            st.session_state.found_words.add(word)
            st.session_state.last_message = f"✅ '{word.upper()}' (+{points} puntos)"
        else:
            st.session_state.last_message = f"❌ '{word.upper()}' no es válida."

        st.session_state.current_word = ""
        st.session_state.word_checked = False

    def update_timer():
        """Actualiza el cronómetro y refresca pantalla sin quedarse en 1 s."""
        if not st.session_state.game_active:
            return

        elapsed = time.time() - st.session_state.start_time
        remaining = 60 - int(elapsed)
        if remaining <= 0:
            st.session_state.time_left = 0
            st.session_state.game_active = False
            st.session_state.round_finished = True
            st.rerun()
        else:
            st.session_state.time_left = remaining
            time.sleep(1)
            st.rerun()

    # ==============================
    # 3️⃣ Interfaz de juego
    # ==============================
    st.title("🧍 Modo Individual")

    # 👇 Iniciar automáticamente la primera ronda
    if not st.session_state.game_active and not st.session_state.round_finished:
        start_game(reset_score=False)
        st.rerun()

    elif st.session_state.game_active:
        st.subheader(f"⏱️ Tiempo restante: {st.session_state.time_left} s")
        st.subheader(f"🔤 Letras: **{st.session_state.letters.upper()}**")
        st.write(f"Puntuación total: **{st.session_state.total_score} puntos**")

        st.text_input("Introduce una palabra:", key="current_word", on_change=check_word)

        # Mostrar palabras encontradas
        if st.session_state.found_words:
            st.markdown("### ✅ Palabras encontradas:")
            palabras_html = ", ".join(sorted(st.session_state.found_words))
            st.markdown(f"<p style='font-size:16px; color:black;'>{palabras_html}</p>", unsafe_allow_html=True)

        #  Mostrar mensaje de validación al final, debajo de la lista
        if st.session_state.last_message:
            msg = st.session_state.last_message
            if msg.startswith("✅"):
                st.success(msg)
            elif msg.startswith("⚠️"):
                st.warning(msg)
            else:
                st.error(msg)
            st.session_state.last_message = ""

        update_timer()

    # ==============================
    # 4️⃣ Fin de ronda
    # ==============================
    if st.session_state.round_finished:
        st.warning("⏱️ ¡Tiempo agotado!")
        st.write(f"🎯 Puntuación total acumulada: **{st.session_state.total_score} puntos**")

        # 📜 Mostrar todas las palabras posibles (sin límite)
        possible_words = [
            w for w in words if all(l in w for l in st.session_state.letters.lower())
        ]
        possible_words = sorted(possible_words)
        with st.expander(f"📜 Ver todas las palabras posibles ({len(possible_words)}):", expanded=False):
            st.text(", ".join(possible_words))

        if len(st.session_state.found_words) == 0:
            st.error("No lograste escribir ninguna palabra 😢")
        else:
            st.success("¡Ronda completada! 👏")

        col1, col2 = st.columns(2)

        # Solo mostrar "Siguiente ronda" si encontró al menos una palabra
        if len(st.session_state.found_words) > 0:
            with col1:
                if st.button("➡️ Siguiente ronda"):
                    full_clean_for_new_round()

        # Siempre mostrar "Volver al inicio"
        with col2:
            if st.button("🏠 Volver al inicio"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.session_state.screen = "start"
                st.rerun()

