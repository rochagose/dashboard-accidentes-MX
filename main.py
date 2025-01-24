import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

#Creando el dataframe a partir de los dos csv generados previamente
part1 = pd.read_csv('data/parte1.csv')
part2 = pd.read_csv('data/parte2.csv')
df = pd.concat([part1, part2]) 

#Configuracion general del dashboard
st.set_page_config(page_title = "Dashboard", 
                   page_icon = "🚦", 
                   layout = "wide",
                   initial_sidebar_state = "collapsed")
alt.themes.enable("dark")
st.subheader("🛑 Incidentes Automovilisticos (CDMX)")
st.markdown("#####")

#Creando barra lateral
with st.sidebar:
    st.image("images/logo.png")
    st.header("Filtros")
    lista_anios = list(df.año_cierre.unique())
    anio_seleccionado = st.selectbox('Seleccione un año', lista_anios)
    df_anio_seleccionado = df[df.año_cierre == anio_seleccionado]

def formatear(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

col = st.columns((3, 2), gap='small')

def Home():
    total_incidentes = df_anio_seleccionado['folio'].count()
    delegacion_mayor_incidentes = df_anio_seleccionado['delegacion_inicio'].mode().iloc[0]
    mes_mayor_incidentes = df_anio_seleccionado['mes_cierre'].mode().iloc[0]
    no_incidentes_afirmativos = df_anio_seleccionado['codigo_cierre'].value_counts().get('A', 0)
    no_incidentes_negativos = df_anio_seleccionado['codigo_cierre'].value_counts().get('N', 0)
    no_incidentes_falsos = df_anio_seleccionado['codigo_cierre'].value_counts().get('F', 0)

    with col[0]:
        kpi1, kpi2, kpi3 = st.columns(3, gap = "small")
        with kpi1:
            st.info("📌 No. Total de Incidentes")
            st.metric(label = "Incidentes", value = formatear(total_incidentes))
        
        with kpi2:
            st.info("📊 Mayor No. de Incidentes")
            st.metric(label = "Delegacion", value = delegacion_mayor_incidentes)

        with kpi3:
            st.info("📆 Mayor No. de Incidentes")
            st.metric(label = "Mes", value = mes_mayor_incidentes)

        kpi4, kpi5, kpi6 = st.columns(3, gap = "small")
        with kpi4:
            st.info("✅ Incidentes Afirmativos")
            st.metric(label = "Afirmativos", value = formatear(no_incidentes_afirmativos))

        with kpi5:
            st.info("❌ Incidentes Negativos")
            st.metric(label = "Negativos", value = formatear(no_incidentes_negativos))

        with kpi6:
            st.info("❗ Incidentes Falsos")
            st.metric(label = "Falsos", value = formatear(no_incidentes_falsos))               
    with col[1]:
        st.markdown("### Top Delegaciones")
        delegaciones = df_anio_seleccionado['delegacion_cierre'].value_counts().reset_index()
        delegaciones.columns = ['Delegación', 'Incidentes'] 

        st.dataframe(delegaciones,
                     use_container_width = True,
                     hide_index = True
                     )

Home()
#Mostrando el dataframe en una tabla
#st.dataframe(df_filter)