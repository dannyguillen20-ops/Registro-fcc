import streamlit as st
import time

st.set_page_config(page_title="SPORT TIME", page_icon="⏱️", layout="wide")

st.markdown("""
<style>
h1{color:#00FF88!important; text-align:center}
.marcador{background:linear-gradient(90deg,#00c6ff,#0072ff); padding:20px; border-radius:15px; text-align:center; color:white; font-size:26px; font-weight:bold; margin:15px 0}
.crono{font-size:80px!important; font-weight:900; text-align:center; color:#00FF88; background:black; padding:30px; border-radius:20px; margin:20px 0}
.ganador{font-size:55px!important; font-weight:900; text-align:center; color:gold; background:linear-gradient(90deg,#000428,#004e92); padding:40px; border-radius:25px; margin:20px 0; border:5px solid gold; animation: pulse 1s infinite}
</style>
""", unsafe_allow_html=True)

st.title("⏱️ SPORT TIME")
st.caption("Control Total")

MODALIDADES = {
    "Fútbol Campo 11 vs 11": {"jug": 11, "arbs": 3, "tag": "Goles"},
    "Fútbol Cancha 7 vs 7": {"jug": 7, "arbs": 2, "tag": "Goles"},
    "Fútbol Sala / Futsal 5 vs 5": {"jug": 5, "arbs": 2, "tag": "Goles"},
    "Básquetbol 5 vs 5": {"jug": 5, "arbs": 3, "tag": "Puntos"},
    "Básquetbol 3x3": {"jug": 3, "arbs": 1, "tag": "Puntos"},
}

MAX_J = 25
if 'g1' not in st.session_state:
    st.session_state.g1=[0]*MAX_J; st.session_state.f1=[0]*MAX_J
    st.session_state.g2=[0]*MAX_J; st.session_state.f2=[0]*MAX_J
    st.session_state.segundos=0; st.session_state.corriendo=False
    st.session_state.ultimo_tiempo=time.time()
    st.session_state.finalizado=False

st.subheader("🏟️ Elige Modalidad")
modalidad = st.selectbox("Modalidad", list(MODALIDADES.keys()))
cfg = MODALIDADES[modalidad]

c_t1,c_t2,c_t3,c_t4 = st.columns(4)
with c_t1:
    periodo = st.selectbox("Periodo", ["Primer Tiempo", "Segundo Tiempo", "Tiempo Extra", "Final"])
with c_t2:
    d1 = st.number_input("Min 1er Tiempo", 1, 60, 10)
with c_t3:
    d2 = st.number_input("Min 2do Tiempo", 1, 60, 10)
with c_t4:
    d_extra = st.number_input("Min Extra", 1, 30, 5)

dur_actual = d1 if periodo=="Primer Tiempo" else d2 if periodo=="Segundo Tiempo" else d_extra
dur_seg = dur_actual*60

# PANTALLA PRINCIPAL
if st.session_state.finalizado:
    # PANTALLA DE CONGRATULATIONS
    eq1_nom = st.session_state.get("eq1_nom_cache", "Equipo 1")
    eq2_nom = st.session_state.get("eq2_nom_cache", "Equipo 2")
    t1 = sum(st.session_state.g1)
    t2 = sum(st.session_state.g2)
    if t1 > t2:
        ganador = eq1_nom
        marcador_f = f"{t1} - {t2}"
    elif t2 > t1:
        ganador = eq2_nom
        marcador_f = f"{t2} - {t1}"
    else:
        ganador = "¡EMPATE!"
        marcador_f = f"{t1} - {t2}"

    st.balloons()
    st.snow()
    if ganador == "¡EMPATE!":
        st.markdown(f"<div class='ganador'>🤝 ¡EMPATE!<br><span style='font-size:30px'>{eq1_nom} {marcador_f} {eq2_nom}</span><br><span style='font-size:20px'>¡Buen Partido!</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ganador'>🏆 CONGRATULATIONS<br><span style='font-size:40px'>{ganador}</span><br><span style='font-size:28px'>Ganó {marcador_f}</span><br><span style='font-size:18px'>{modalidad}</span></div>", unsafe_allow_html=True)

    if st.button("🔄 Nuevo Partido", use_container_width=True, type="primary"):
        st.session_state.g1=[0]*MAX_J; st.session_state.f1=[0]*MAX_J
        st.session_state.g2=[0]*MAX_J; st.session_state.f2=[0]*MAX_J
        st.session_state.segundos=0; st.session_state.corriendo=False; st.session_state.finalizado=False
        st.rerun()
else:
    # CRONO NORMAL
    mins = st.session_state.segundos // 60
    segs = st.session_state.segundos % 60
    tiempo_str = f"{mins:02d}:{segs:02d}"
    st.markdown(f"<div class='crono'>{tiempo_str} / {dur_actual:02d}:00<br><span style='font-size:18px'>{modalidad} - {periodo}</span></div>", unsafe_allow_html=True)

    cc1,cc2,cc3 = st.columns(3)
    with cc1:
        if st.button("▶️ INICIAR", use_container_width=True, type="primary"):
            st.session_state.corriendo=True; st.session_state.ultimo_tiempo=time.time(); st.rerun()
    with cc2:
        if st.button("⏸️ PAUSAR", use_container_width=True):
            st.session_state.corriendo=False; st.rerun()
    with cc3:
        if st.button("🔄 REINICIAR TIEMPO", use_container_width=True):
            st.session_state.segundos=0; st.session_state.corriendo=False; st.rerun()

    if st.session_state.corriendo:
        if time.time() - st.session_state.ultimo_tiempo >= 1:
            st.session_state.segundos+=1; st.session_state.ultimo_tiempo=time.time()
            if st.session_state.segundos >= dur_seg:
                st.session_state.segundos=dur_seg; st.session_state.corriendo=False
                if periodo in ["Segundo Tiempo", "Tiempo Extra", "Final"]:
                    st.session_state.finalizado=True
                st.balloons()
        time.sleep(0.1); st.rerun()

    # ARBITROS
    st.divider()
    cols_arb = st.columns(cfg['arbs'])
    arbitros=[]
    for i in range(cfg['arbs']):
        with cols_arb[i]:
            a = st.text_input(f"Árbitro {i+1}", "", key=f"arb_{i}")
            arbitros.append(a)
    arbitros_txt = " - ".join([a for a in arbitros if a])

    # JUGADORES
    num_jugadores = st.number_input(f"Jugadores por equipo (defecto {cfg['jug']})", 1, 20, cfg['jug'])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"🔵 Equipo 1")
        eq1 = st.text_input("Nombre Eq1", "Equipo 1", key="eq1")
        st.session_state.eq1_nom_cache = eq1
        for i in range(num_jugadores):
            with st.container(border=True):
                st.text_input("Nombre", key=f"n1_{i}", placeholder=f"Jugador {i+1}", label_visibility="collapsed")
                c1,c2,c3 = st.columns([2,1,1])
                with c1: st.write(f"{cfg['tag']}: {st.session_state.g1[i]}")
                with c2:
                    if st.button(f"+ {cfg['tag']}", key=f"g1_{i}"): st.session_state.g1[i]+=1; st.rerun()
                with c3:
                    if st.button("Falta", key=f"f1_{i}"): st.session_state.f1[i]+=1; st.rerun()

    with col2:
        st.subheader(f"🔴 Equipo 2")
        eq2 = st.text_input("Nombre Eq2", "Equipo 2", key="eq2")
        st.session_state.eq2_nom_cache = eq2
        for i in range(num_jugadores):
            with st.container(border=True):
                st.text_input("Nombre", key=f"n2_{i}", placeholder=f"Jugador {i+1}", label_visibility="collapsed")
                c1,c2,c3 = st.columns([2,1,1])
                with c1: st.write(f"{cfg['tag']}: {st.session_state.g2[i]}")
                with c2:
                    if st.button(f"+ {cfg['tag']}", key=f"g2_{i}"): st.session_state.g2[i]+=1; st.rerun()
                with c3:
                    if st.button("Falta", key=f"f2_{i}"): st.session_state.f2[i]+=1; st.rerun()

    t1 = sum(st.session_state.g1[:num_jugadores]); t2 = sum(st.session_state.g2[:num_jugadores])
    st.markdown(f"<div class='marcador'>{eq1} {t1} - {t2} {eq2} | {periodo} {tiempo_str} | {arbitros_txt}</div>", unsafe_allow_html=True)

    if st.button("🏁 FINALIZAR PARTIDO - CONGRATULATIONS", type="primary", use_container_width=True):
        st.session_state.finalizado=True
        st.balloons()
        st.rerun()
