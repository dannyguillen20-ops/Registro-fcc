import streamlit as st

st.set_page_config(page_title="SPORT TIME", page_icon="⏱️", layout="wide")

st.markdown("""
<style>
h1{color:#00FF88!important; text-align:center}
.marcador{background:linear-gradient(90deg,#00c6ff,#0072ff); padding:20px; border-radius:15px; text-align:center; color:white; font-size:26px; font-weight:bold; margin:15px 0}
</style>
""", unsafe_allow_html=True)

st.title("⏱️ SPORT TIME")
st.caption("Raymundo Enríquez - Control Total")

if 'g1' not in st.session_state:
    st.session_state.g1=[0]*7
    st.session_state.f1=[0]*7
    st.session_state.g2=[0]*7
    st.session_state.f2=[0]*7

c1,c2,c3,c4 = st.columns(4)
with c1:
    deporte = st.selectbox("Deporte", ["Fútbol Soccer", "Básquetbol"])
with c2:
    periodo = st.selectbox("Periodo", ["Primer Tiempo", "Segundo Tiempo", "Tiempo Extra", "Final"])
with c3:
    minuto = st.number_input("Minuto", 0, 120, 0)
with c4:
    extra = st.number_input("Extra +", 0, 20, 0)

is_fut = deporte == "Fútbol Soccer"
num = 7 if is_fut else 5
label = "Goles" if is_fut else "Puntos"

c_a1,c_a2,c_a3 = st.columns(3)
with c_a1:
    arb1 = st.text_input("Árbitro Central", "Raymundo")
with c_a2:
    arb2 = st.text_input("Árbitro 2", "")
with c_a3:
    cancha = st.text_input("Cancha", "Raymundo Enríquez")

col1, col2 = st.columns(2)

# EQUIPO 1
with col1:
    st.subheader("🔵 Equipo 1")
    eq1_nom = st.text_input("Nombre Equipo 1", "Raymundo FC", key="eq1_nom")
    for i in range(num):
        with st.container(border=True):
            nom = st.text_input(f"Jugador {i+1}", key=f"n1_{i}", placeholder=f"Jugador {i+1}", label_visibility="collapsed")
            cc1, cc2 = st.columns(2)
            with cc1:
                st.write(f"{label}: {st.session_state.g1[i]}")
                if st.button(f"+ {label}", key=f"g1_{i}"):
                    st.session_state.g1[i]+=1
                    st.rerun()
            with cc2:
                st.write(f"Faltas: {st.session_state.f1[i]}")
                if st.button("Falta +", key=f"f1_{i}"):
                    st.session_state.f1[i]+=1
                    st.rerun()

# EQUIPO 2
with col2:
    st.subheader("🔴 Equipo 2")
    eq2_nom = st.text_input("Nombre Equipo 2", "Rival FC", key="eq2_nom")
    for i in range(num):
        with st.container(border=True):
            nom = st.text_input(f"Jugador {i+1}", key=f"n2_{i}", placeholder=f"Jugador {i+1}", label_visibility="collapsed")
            cc1, cc2 = st.columns(2)
            with cc1:
                st.write(f"{label}: {st.session_state.g2[i]}")
                if st.button(f"+ {label}", key=f"g2_{i}"):
                    st.session_state.g2[i]+=1
                    st.rerun()
            with cc2:
                st.write(f"Faltas: {st.session_state.f2[i]}")
                if st.button("Falta +", key=f"f2_{i}"):
                    st.session_state.f2[i]+=1
                    st.rerun()

t1 = sum(st.session_state.g1[:num])
t2 = sum(st.session_state.g2[:num])

st.markdown(f"<div class='marcador'>{eq1_nom} {t1} - {t2} {eq2_nom} | {periodo} {minuto}' +{extra} | Cancha: {cancha} | Arb: {arb1}</div>", unsafe_allow_html=True)

b1,b2 = st.columns(2)
with b1:
    if st.button("🔄 Reiniciar Partido", use_container_width=True):
        st.session_state.g1=[0]*7
        st.session_state.f1=[0]*7
        st.session_state.g2=[0]*7
        st.session_state.f2=[0]*7
        st.rerun()
with b2:
    if st.button("🏁 Finalizar Reta", type="primary", use_container_width=True):
        st.balloons()
        st.success(f"Final: {eq1_nom} {t1} - {t2} {eq2_nom}")
