import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SPORT TIME", page_icon="⏱️", layout="wide")

# --- ESTILOS CON COLOR ---
st.markdown("""
<style>
   .stApp { background-color: #0e1117; }
    h1 { color: #00FF88!important; text-align: center; }
   .marcador { background: linear-gradient(90deg, #00c6ff, #0072ff); padding: 20px; border-radius: 15px; text-align: center; color: white; font-size: 28px; font-weight: bold; }
   .equipo1 { background-color: #1e3a8a; padding: 15px; border-radius: 10px; }
   .equipo2 { background-color: #991b1b; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("⏱️ SPORT TIME")
st.markdown("<p style='text-align:center; color:gray;'>Control Total de Retas - Tapachula</p>", unsafe_allow_html=True)

# --- ESTADO ---
if 'goles_eq1' not in st.session_state:
    st.session_state.goles_eq1 = [0]*10
    st.session_state.faltas_eq1 = [0]*10
    st.session_state.goles_eq2 = [0]*10
    st.session_state.faltas_eq2 = [0]*10
    st.session_state.tiempo = 0
    st.session_state.tiempo_extra = 0
    st.session_state.periodo = "Primer Tiempo"

# --- CONFIGURACION SUPERIOR ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    deporte = st.selectbox("🏀 / ⚽ Deporte", ["Fútbol Soccer", "Básquetbol"])
with c2:
    periodo = st.selectbox("⏱️ Periodo", ["Primer Tiempo", "Segundo Tiempo", "Tiempo Extra", "Finalizado"], key="periodo_sel")
with c3:
    tiempo = st.number_input("Minuto Actual", 0, 120, st.session_state.tiempo)
    st.session_state.tiempo = tiempo
with c4:
    tiempo_extra = st.number_input("Tiempo Extra (+)", 0, 20, st.session_state.tiempo_extra)
    st.session_state.tiempo_extra = tiempo_extra

es_futbol = deporte == "Fútbol Soccer"
num_jugadores = 7 if es_futbol else 5
label_gol = "Goles" if es_futbol else "Puntos"

c_ar1, c_ar2, c_ar3 = st.columns(3)
with c_ar1:
    arbitro1 = st.text_input("👨‍⚖️ Árbitro Central", "Raymundo")
with c_ar2:
    arbitro2 = st.text_input("🚩 Asistente 1 / Árbitro 2", "")
with c_ar3:
    cancha = st.text_input("📍 Cancha", "Raymundo Enríquez")

st.divider()

# --- EQUIPOS ---
col1, col2 = st.columns(2)

def dibujar_equipo(col, num_eq, nombre_default, color):
    with col:
        st.markdown(f"### {color} EQUIPO {num_eq}")
        nombre_eq = st.text_input(f"Nombre Equipo {num_eq}", nombre_default, key=f"nom_eq{num_eq}")

        goles_key = st.session_state.goles_eq1 if num_eq==1 else st.session_state.goles_eq2
        faltas_key = st.session_state.faltas_eq1 if num_eq==1 else st.session_state.faltas_eq2

        total_goles = 0
        total_faltas = 0
        jugadores_data = []

        for i in range(num_jugadores):
            with st.container(border=True):
                c_n, c_g, c_f = st.columns([2,1,1])
                with c_n:
                    nom = st.text_input(f"Jugador {i+1}", key=f"eq{num_eq}_n{i}", placeholder=f"Jugador {i+1}", label_visibility="collapsed")
                    if not nom: nom = f"Jugador {i+1}"
                with c_g:
                    st.caption(f"{label_gol}: {goles_key[i]}")
                    if st.button(f"⚽ +{label_gol}", key=f"g_eq{num_eq}_{i}"):
                        if num_eq==1: st.session_state.goles_eq1[i]+=1
                        else: st.session_state.goles_eq2[i]+=1
                        st.rerun()
                    if st.button(f"-", key=f"gm_eq{num_eq}_{i}"):
                        if num_eq==1 and st.session_state.goles_eq1[i]>0: st.session_state.goles_eq1[i]-=1
                        if num_eq==2 and st.session_state.goles_eq2[i]>0: st.session_state.goles_eq2[i]-=1
                        st.rerun()
                with c_f:
                    st.caption(f"Faltas: {faltas_key[i]}")
                    if st.button("🟨 Falta", key=f"f_eq{num_eq}_{i}"):
                        if num_eq==1: st.session_state.faltas_eq1[i]+=1
                        else: st.session_state.faltas_eq2[i]+=1
                        st.rerun()

                total_goles += goles_key[i]
                total_faltas += faltas_key[i]
                jugadores_data.append(nom)

        return nombre_eq, total_goles, total_faltas, jugadores_data

eq1_nom, tot1, fal1, jug1 = dibujar_equipo(col1, 1, "Raymundo FC", "🔵")
eq2_nom, tot2, fal2, jug2 = dibujar_equipo(col2, 2, "Rival FC", "🔴")

st.divider()

# --- MARCADOR CENTRAL ---
st.markdown(f"<div class='marcador'>{eq1_nom} {tot1} - {tot2} {eq2_nom} | {periodo} {tiempo}' + {tiempo_extra}' | {cancha}</div>", unsafe_allow_html=True)

st.write("")
col_mid1, col_mid2, col_mid3 = st.columns(3)
with col_mid1:
    st.metric(f"{eq1_nom} - {label_gol}", tot1, f"Faltas: {fal1}")
with col_mid2:
    st.metric("Árbitros", arbitro1, arbitro2)
with col_mid3:
    st.metric(f"{eq2_nom} - {label_gol}", tot2, f"Faltas: {fal2}")

# --- TABLA DETALLADA ---
data = []
for i in range(num_jugadores):
    data.append({"Equipo": eq1_nom, "Jugador": jug1[i], label_gol: st.session_state.goles_eq1[i], "Faltas": st.session_state.faltas_eq1[i]})
    data.append({"Equipo": eq2_nom, "Jugador": jug2[i], label_gol: st.session_state.goles_eq2[i], "Faltas": st.session_state.faltas_eq2[i]})

df = pd.DataFrame(data)
df = df.sort_values(by=label_gol, ascending=False)
st.markdown(f"### 📊 Estadísticas Completas - {deporte}")
st.dataframe(df, use_container_width=True, hide_index=True)

if st.button("🏁 Finalizar Partido y Compartir", type="primary", use_container_width=True):
    st.balloons()
    st.success(f"PARTIDO FINALIZADO: {eq1_nom} {tot1}-{tot2} {eq2_nom} | Árbitro: {arbitro1}")
    texto_whatsapp = f"SPORT TIME: {eq1_nom} {tot1}-{tot2} {eq2_nom} - {periodo} - Goleador: {df.iloc[0]['Jugador']}"
    st.code(texto_whatsapp, language="text")
    st.info("Copia ese texto y mándalo por WhatsApp a tus compas")

if st.button("🔄 Reiniciar Todo el Partido", use_container_width=True):
    st.session_state.goles_eq1 = [0]*10
    st.session_state.faltas_eq1 = [0]*10
    st.session_state.goles_eq2 = [0]*10
    st.session_state.faltas_eq2 = [0]*10
    st.session_state.tiempo = 0
    st.rerun()
