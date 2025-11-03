import pickle
import streamlit as st

# ===============================
# 🔹 Cargar el diccionario solo una vez
# ===============================
@st.cache_data
def cargar_palabras():
    with open("modes/palabras.pkl", "rb") as f:
        return pickle.load(f)

palabras = cargar_palabras()


# ===============================
# 🔹 Función auxiliar
# ===============================
def contiene_letras(palabra, letras):
    """Las letras pueden aparecer en cualquier orden."""
    return all(letra in palabra for letra in letras)


# ===============================
# 🔹 Función principal del modo multijugador
# ===============================
def run_mode():
    # Inicializar variables de sesión si no existen
    for clave, valor in {
        "fase": "config",
        "jugadores": {},
        "letras": "",
        "palabras_usadas": set(),
        "ultimo_resultado": "",
        "ultima_accion": None
    }.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor

    # ===============================
    # 👥 Fase 3: Configuración de jugadores
    # ===============================
    if st.session_state.fase == "config":
        st.title("👥 Configuración de jugadores")

        num = st.number_input("Número de jugadores:", min_value=1, max_value=10, value=2)
        nombres = []
        with st.form("form_nombres"):
            for i in range(num):
                nombre = st.text_input(f"Nombre del jugador {i+1}:").strip()
                nombres.append(nombre)
            enviado = st.form_submit_button("✅ Confirmar jugadores")

        if enviado:
            st.session_state.jugadores = {n: 0 for n in nombres if n}
            if st.session_state.jugadores:
                st.session_state.fase = "juego"
                st.rerun()
            else:
                st.warning("Debes introducir al menos un nombre válido.")

    # ===============================
    # 🎮 Fase 4: Juego principal
    # ===============================
    elif st.session_state.fase == "juego":
        st.title("🎮 ABC GAME - Multijugador")

        # Introducción de letras
        letras = st.text_input("Letras de la matrícula (3 letras):", value=st.session_state.letras).strip().lower()
        if letras and len(letras) == 3 and letras.isalpha():
            st.session_state.letras = letras
            st.write(f"Letras activas: **{letras.upper()}**")

            # Seleccionar jugador y palabra
            jugador = st.selectbox("Selecciona el jugador:", list(st.session_state.jugadores.keys()))
            palabra = st.text_input("Introduce la palabra propuesta:").strip().lower()

            if st.button("🧩 Comprobar palabra"):
                if not palabra:
                    st.session_state.ultimo_resultado = "⚠️ Introduce una palabra."
                elif palabra in st.session_state.palabras_usadas:
                    st.session_state.ultimo_resultado = f"⚠️ La palabra '{palabra}' ya fue utilizada."
                elif palabra in palabras and contiene_letras(palabra, letras):
                    st.session_state.palabras_usadas.add(palabra)
                    st.session_state.jugadores[jugador] += 1
                    st.session_state.ultimo_resultado = f"🧩 Palabra válida: '{palabra.upper()}' (+1 punto para {jugador})"
                else:
                    st.session_state.palabras_usadas.add(palabra)
                    st.session_state.ultimo_resultado = f"❌ '{palabra.upper()}' no existe o no contiene todas las letras."

                st.session_state.ultima_accion = True

        elif letras:
            st.warning("Introduce exactamente 3 letras válidas.")

        # Mostrar resultado
        if st.session_state.ultimo_resultado:
            msg = st.session_state.ultimo_resultado
            if msg.startswith("🧩"):
                st.success(msg)
            elif msg.startswith("⚠️"):
                st.warning(msg)
            else:
                st.error(msg)

        # Marcador
        if st.session_state.ultima_accion or any(st.session_state.jugadores.values()):
            st.divider()
            st.subheader("🏆 Marcador")
            for nombre, puntos in sorted(st.session_state.jugadores.items(), key=lambda x: x[1], reverse=True):
                st.write(f"{nombre}: {puntos} puntos")
            st.session_state.ultima_accion = False

        # Ver palabras válidas
        if st.session_state.letras:
            with st.expander("📜 Ver todas las palabras válidas para estas letras"):
                posibles = [p for p in palabras if contiene_letras(p, st.session_state.letras)]
                if posibles:
                    st.write(f"Se encontraron {len(posibles)} palabras:")
                    st.text(", ".join(sorted(posibles)))
                else:
                    st.warning("No hay palabras con ese patrón.")

        # Reiniciar
        st.divider()
        if st.button("🔁 Reiniciar partida"):
            for k in ["jugadores", "letras", "palabras_usadas", "ultimo_resultado", "ultima_accion", "fase"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.screen = "start"
            st.success("🔁 Partida reiniciada. Volviendo al inicio...")
            st.rerun()
