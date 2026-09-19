import streamlit as st

st.title("⚽ Reta Oficial - Raymundo Enríquez - V5 FINAL")

nombre_equipo = st.text_input("Nombre de tu equipo", "Raymundo Enríquez FC")
nombre_rival = st.text_input("Nombre del rival", "Equipo Rival")
cantidad = st.number_input("¿Cuántos jugadores en tu equipo?", 1, 30, 4)

if "jugadores" not in st.session_state:
    st.session_state.jugadores = []
if "goles_local" not in st.session_state:
    st.session_state.goles_local = 0
if "goles_rival" not in st.session_state:
    st.session_state.goles_rival = 0

jugadores_temp = []
st.divider()
st.write(f"### Plantilla {nombre_equipo}")

for i in range(int(cantidad)):
    col1, col2, col3 = st.columns([1,2,2])
    with col1:
        dorsal = st.number_input(f"Dorsal", 1, 99, i+1, key=f"d{i}")
    with col2:
        nombre = st.text_input(f"Nombre", key=f"n{i}")
    with col3:
        pos = st.selectbox(f"Pos", ["Portero","Defensa","Medio","Delantero"], key=f"p{i}")
    if nombre:
        faltas = 0
        goles = 0
        for j in st.session_state.jugadores:
            if j["nombre"] == nombre:
                faltas = j["faltas"]
                goles = j["goles"]
        jugadores_temp.append({
            "numero": dorsal, "nombre": nombre, "posicion": pos,
            "faltas": faltas, "goles": goles
        })

if st.button("Guardar plantilla"):
    st.session_state.jugadores = jugadores_temp
    st.success("Plantilla guardada")

st.divider()
st.write("### 📊 Marcador por Equipo")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(nombre_equipo, st.session_state.goles_local)
    if st.button(f"Gol {nombre_equipo} +1"):
        st.session_state.goles_local += 1
        st.rerun()
with c2:
    st.write("VS")
    if st.button("Reiniciar todo"):
        st.session_state.goles_local = 0
        st.session_state.goles_rival = 0
        for j in st.session_state.jugadores:
            j["faltas"] = 0
            j["goles"] = 0
        st.rerun()
with c3:
    st.metric(nombre_rival, st.session_state.goles_rival)
    if st.button(f"Gol {nombre_rival} +1"):
        st.session_state.goles_rival += 1
        st.rerun()

st.divider()
st.write(f"### 📋 Jugadores de {nombre_equipo} - Goles y Faltas")

if st.session_state.jugadores:
    for idx, j in enumerate(st.session_state.jugadores):
        st.write(f"**#{j['numero']} {j['nombre']} ({j['posicion']})** - Goles: {j['goles']} | Faltas: {j['faltas']}")
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"Gol +1 {j['nombre']}", key=f"g{idx}"):
                st.session_state.jugadores[idx]["goles"] += 1
                st.session_state.goles_local += 1
                st.rerun()
        with b2:
            if st.button(f"Falta +1 {j['nombre']}", key=f"f{idx}"):
                st.session_state.jugadores[idx]["faltas"] += 1
                st.rerun()
else:
    st.info("Guarda tu plantilla primero")
