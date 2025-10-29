import pickle
import streamlit as st

# ===============================
# 🔹 Cargar el diccionario una sola vez
# ===============================
@st.cache_data
def cargar_palabras():
    with open("palabras.pkl", "rb") as f:
        return pickle.load(f)

palabras = cargar_palabras()

# ===============================
# 🔹 Función auxiliar
# ===============================
def contiene_en_orden(palabra, letras):
    i = 0
    for letra in palabra:
        if letra == letras[i]:
            i += 1
            if i == len(letras):
                return True
    return False

# ===============================
# 🔹 Inicialización del estado
# ===============================
if "fase" not in st.session_state:
    st.session_state.fase = "inicio"
if "jugadores" not in st.session_state:
    st.session_state.jugadores = {}
if "letras" not in st.session_state:
    st.session_state.letras = ""
if "palabra_actual" not in st.session_state:
    st.session_state.palabra_actual = ""
if "jugador_actual" not in st.session_state:
    st.session_state.jugador_actual = ""
if "palabras_usadas" not in st.session_state:
    st.session_state.palabras_usadas = set()
if "ultimo_resultado" not in st.session_state:
    st.session_state.ultimo_resultado = ""

# ===============================
# 🔹 Fase 1: Inicio
# ===============================
if st.session_state.fase == "inicio":
    st.title("🔤 ABC GAME")
    st.write("Compite con tus amigos para encontrar palabras válidas con las letras de una matrícula 🚗")

    if st.button("🚀 Start"):
        st.session_state.fase = "instrucciones"
        st.rerun()

# ===============================
# 🔹 Fase 2: Instrucciones
# ===============================
elif st.session_state.fase == "instrucciones":
    st.title("📘 Instrucciones del Juego")

    st.markdown(
        """
        ### 🚗 Objetivo del juego  
        Con las **tres letras** de una matrícula (por ejemplo, `C S A`), los jugadores deben proponer palabras
        del diccionario español que **contengan esas letras en el mismo orden**.  
        Ejemplo: para `C S A`, palabras válidas serían **CASA**, **COSTA** o **Cosecha**.

        ### 🕹️ Dinámica
        1. Introduce las tres letras de la matrícula.  
        2. Cada jugador, por turnos, escribe una palabra y selecciona su nombre.  
        3. Si la palabra es válida y existe en el diccionario → gana **1 punto**.  

        ### 🔁 Fin del juego
        Puedes reiniciar en cualquier momento para volver al inicio y crear una nueva partida.
        """
    )

    st.info("💡 Consejo: no se distingue entre mayúsculas o minúsculas, y las letras deben estar en orden.")

    if st.button("➡️ Continuar"):
        st.session_state.fase = "config"
        st.rerun()

# ===============================
# 🔹 Fase 3: Configuración de jugadores
# ===============================
elif st.session_state.fase == "config":
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
# 🔹 Fase 4: Juego principal
# ===============================
elif st.session_state.fase == "juego":
    st.title("🎮 Juego de las Matrículas")

    # ===== Clasificación =====
    st.subheader("🏆 Clasificación actual")
    ranking = sorted(st.session_state.jugadores.items(), key=lambda x: x[1], reverse=True)
    for nombre, puntos in ranking:
        st.write(f"{nombre}: {puntos} puntos")

    st.divider()

    # ===== Introducción de letras =====
    letras_usuario = st.text_input(
        "Letras de la matrícula (3 letras):",
        st.session_state.letras,
        key="input_letras"
    )

    if letras_usuario:
        st.session_state.letras = letras_usuario.strip().lower()

        if len(st.session_state.letras) == 3 and st.session_state.letras.isalpha():
            st.write(f"Letras activas: **{st.session_state.letras.upper()}**")

            st.subheader("🗣️ Turno del jugador")

            jugador = st.selectbox(
                "Selecciona el jugador que introduce la palabra:",
                list(st.session_state.jugadores.keys()),
                key="jugador_selector"
            )

            palabra = st.text_input(
                "Introduce la palabra propuesta:",
                key="palabra_input"
            ).strip().lower()

            # ====== Botón comprobar palabra ======
            if st.button("🧩 Comprobar palabra"):
                letras = st.session_state.letras

                if not palabra or not letras or len(letras) != 3:
                    st.session_state.ultimo_resultado = "⚠️ Introduce tres letras válidas y una palabra."
                elif palabra in st.session_state.palabras_usadas:
                    st.session_state.ultimo_resultado = f"⚠️ La palabra '{palabra}' ya fue utilizada."
                elif palabra in palabras and contiene_en_orden(palabra, letras):
                    st.session_state.palabras_usadas.add(palabra)
                    st.session_state.jugadores[jugador] += 1
                    st.session_state.ultimo_resultado = f"🧩 Palabra válida: '{palabra.upper()}' (+1 punto para {jugador})"
                else:
                    st.session_state.palabras_usadas.add(palabra)
                    st.session_state.ultimo_resultado = f"❌ No existe la palabra '{palabra.upper()}' o no sigue el orden de letras."

            # ===== Mostrar resultado =====
            if st.session_state.ultimo_resultado:
                msg = st.session_state.ultimo_resultado
                if msg.startswith("🧩"):
                    st.success(msg)
                elif msg.startswith("⚠️"):
                    st.warning(msg)
                else:
                    st.error(msg)

            # 🔄 Redibujar marcador en tiempo real
            st.subheader("🏆 Marcador actualizado")
            for nombre, puntos in st.session_state.jugadores.items():
                st.write(f"{nombre}: {puntos} puntos")

        else:
            st.warning("Introduce exactamente **3 letras** válidas (A-Z).")

    # ===== Ver palabras válidas =====
    if st.session_state.letras:
        letras = st.session_state.letras
        with st.expander("📜 Ver todas las palabras válidas para estas letras"):
            palabras_validas = [p for p in palabras if contiene_en_orden(p, letras)]
            if palabras_validas:
                st.write(f"Se encontraron **{len(palabras_validas)}** palabras que contienen '{letras.upper()}' en orden:")
                st.text(", ".join(sorted(palabras_validas)))
            else:
                st.warning(f"No hay palabras en el diccionario con '{letras.upper()}' en ese orden.")

    # ===== Reiniciar partida =====
    st.divider()
    if st.button("🔁 Reiniciar partida"):
        for clave in ["jugadores", "letras", "palabra_actual", "jugador_actual",
                      "ultimo_resultado", "palabras_usadas"]:
            if clave in st.session_state:
                del st.session_state[clave]
        st.session_state.fase = "inicio"
        st.success("🔁 Partida reiniciada. Volviendo al inicio...")
        st.rerun()



