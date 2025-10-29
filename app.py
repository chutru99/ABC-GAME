import pickle
import streamlit as st

# ===============================
# 🔹 Cargar el diccionario solo una vez
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
# 🔹 Inicializar variables de sesión
# ===============================
for clave, valor in {
    "fase": "inicio",
    "jugadores": {},
    "letras": "",
    "palabras_usadas": set(),
    "ultimo_resultado": "",
    "ultima_accion": None
}.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


# ===============================
# 🔹 Fase 1: Inicio
# ===============================
if st.session_state.fase == "inicio":
    st.title("🔤 Juego de las Matrículas")
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
        4. Una palabra solo se puede usar **una vez** durante toda la partida.

        ### 🔁 Fin del juego
        Puedes reiniciar en cualquier momento para volver al inicio y crear una nueva partida.
        """
    )
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

    # Mostrar clasificación
    st.subheader("🏆 Clasificación actual")
    for nombre, puntos in sorted(st.session_state.jugadores.items(), key=lambda x: x[1], reverse=True):
        st.write(f"{nombre}: {puntos} puntos")

    st.divider()

    # Introducir letras
    letras = st.text_input("Letras de la matrícula (3 letras):", value=st.session_state.letras).strip().lower()
    if letras and len(letras) == 3 and letras.isalpha():
        st.session_state.letras = letras
        st.write(f"Letras activas: **{letras.upper()}**")

        # Seleccionar jugador y palabra
        jugador = st.selectbox("Selecciona el jugador:", list(st.session_state.jugadores.keys()))
        palabra = st.text_input("Introduce la palabra propuesta:").strip().lower()

        # Comprobar palabra
        if st.button("🧩 Comprobar palabra"):
            if not palabra:
                st.session_state.ultimo_resultado = "⚠️ Introduce una palabra."
            elif palabra in st.session_state.palabras_usadas:
                st.session_state.ultimo_resultado = f"⚠️ La palabra '{palabra}' ya fue utilizada."
            elif palabra in palabras and contiene_en_orden(palabra, letras):
                st.session_state.palabras_usadas.add(palabra)
                st.session_state.jugadores[jugador] += 1
                st.session_state.ultimo_resultado = f"🧩 Palabra válida: '{palabra.upper()}' (+1 punto para {jugador})"
            else:
                st.session_state.palabras_usadas.add(palabra)
                st.session_state.ultimo_resultado = f"❌ '{palabra.upper()}' no existe o no sigue el orden de letras."

            st.session_state.ultima_accion = True  # bandera para redibujar

    elif letras:
        st.warning("Introduce exactamente 3 letras válidas.")

    # Mostrar resultado (solo si se jugó)
    if st.session_state.ultimo_resultado:
        msg = st.session_state.ultimo_resultado
        if msg.startswith("🧩"):
            st.success(msg)
        elif msg.startswith("⚠️"):
            st.warning(msg)
        else:
            st.error(msg)

    # Redibujar el marcador inmediatamente
    if st.session_state.ultima_accion:
        st.divider()
        st.subheader("🏆 Marcador actualizado")
        for nombre, puntos in sorted(st.session_state.jugadores.items(), key=lambda x: x[1], reverse=True):
            st.write(f"{nombre}: {puntos} puntos")
        st.session_state.ultima_accion = False

    # Palabras posibles
    if st.session_state.letras:
        with st.expander("📜 Ver todas las palabras válidas para estas letras"):
            posibles = [p for p in palabras if contiene_en_orden(p, st.session_state.letras)]
            if posibles:
                st.write(f"Se encontraron {len(posibles)} palabras:")
                st.text(", ".join(sorted(posibles)))
            else:
                st.warning("No hay palabras con ese patrón.")

    # Reiniciar partida
    st.divider()
    if st.button("🔁 Reiniciar partida"):
        for k in ["jugadores", "letras", "palabras_usadas", "ultimo_resultado", "ultima_accion"]:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state.fase = "inicio"
        st.success("🔁 Partida reiniciada. Volviendo al inicio...")
        st.rerun()




