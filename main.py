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

#Creando barra lateral
with st.sidebar:
    st.image("images/logo.png")
    st.header("Filtros")
    lista_anios = list(df.año_cierre.unique())
    lista_delegaciones = list(df.delegacion_cierre.unique())
    lista_codigo = list(df.codigo_cierre.unique())
    lista_clas_c4 = list(df.incidente_c4.unique())
    lista_alarma = list(df.clas_con_f_alarma.unique())
    lista_entrada = list(df.tipo_entrada.unique())
    

    anio_seleccionado = st.selectbox('Seleccione un año', lista_anios)
    df_anio_seleccionado = df[df.año_cierre == anio_seleccionado]
    delegacion_seleccionada = st.selectbox('Seleccione una delegacion', lista_delegaciones)
    codigo_selecionado = st.selectbox('Seleccione un codigo', lista_codigo)
    clas_seleccionada = st.selectbox('Seleccione una clasificacion', lista_clas_c4)
    alarma_seleccionada = st.selectbox('Seleccione la clase de alarma', lista_alarma)
    entrada_seleccionada = st.selectbox('Seleccione un tipo de entrada', lista_entrada)
    
    df_filtrado = df[(df.año_cierre == anio_seleccionado) &
                    (df.delegacion_cierre == delegacion_seleccionada) &
                    (df.codigo_cierre == codigo_selecionado) &
                    (df.incidente_c4 == clas_seleccionada) &
                    (df.clas_con_f_alarma == alarma_seleccionada) &
                    (df.tipo_entrada == entrada_seleccionada)]
    

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
            st.info("❗ Incidentes Falsos Registrados")
            st.metric(label = "Falsos", value = formatear(no_incidentes_falsos))               
    with col[1]:
        st.markdown(f"### 🌎 Top Delegaciones ({anio_seleccionado})")
        delegaciones = df_anio_seleccionado['delegacion_cierre'].value_counts().reset_index()
        delegaciones = delegaciones.head(5)
        delegaciones.columns = ['Delegación', 'Incidentes'] 

        st.dataframe(delegaciones,
                     use_container_width = True,
                     hide_index = True
                     )
    
    st.subheader("📁 Base de Datos: Incidentes 2017 a 2019")
    df_tabla = df_filtrado[['folio', 'codigo_cierre', 'delegacion_inicio', 'incidente_c4', 'clas_con_f_alarma', 'tipo_entrada', 'año_cierre']]
    df_tabla.columns = ['Folio', 'Codigo', 'Delegacion', 'Clasificacion del C4', 'Clasificacion de la Alarma', 'Canal de Reporte', 'Año ']

    with st.expander('Visualizar base de datos'):
        st.dataframe(df_tabla,
                    use_container_width = True, 
                    hide_index = True,
                    on_select = "ignore")
    
    st.subheader("📈 Gráficas")
    col_g = st.columns(2, gap = "small")
    #Graficar
    with col_g[0]:
        with st.container(border = True):
            frecuencia = df_anio_seleccionado['delegacion_cierre'].value_counts().reset_index()
            frecuencia.columns = ['Delegacion', 'Frecuencia']
            st.subheader(f"Frecuencia por delegacion ({anio_seleccionado})")
            st.bar_chart(frecuencia, x = 'Delegacion', y = 'Frecuencia', x_label = 'Delegacion', y_label = 'Frecuencia',
            horizontal = False)
    with col_g[1]:
        with st.container(border = True):
            freq_canal_reporte = df_anio_seleccionado['tipo_entrada'].value_counts().reset_index()
            freq_canal_reporte.columns = ['Canal de Reporte', 'Frecuencia']
            st.subheader(f"Frecuencia por canal de reporte ({anio_seleccionado})")
            st.bar_chart(freq_canal_reporte, x = 'Canal de Reporte', y = 'Frecuencia', x_label = 'Canal', y_label = 'Frecuencia',
            horizontal = False)

    colg_g_2 = st.columns(2, gap = "small")
    with colg_g_2[0]:
        with st.container(border = True):
            freq_clasificacion = df_anio_seleccionado['codigo_cierre'].value_counts().reset_index()
            freq_clasificacion.columns = ['Clasificacion', 'Frecuencia']
            st.subheader(f"Frecuencia por clasificacion de cierre ({anio_seleccionado})")
            st.bar_chart(freq_clasificacion, x = 'Clasificacion', y = 'Frecuencia', x_label = 'Clasificacion', y_label = 'Frecuencia',
            horizontal = False)
    with colg_g_2[1]:
        with st.container(border = True):
            freq_alarma = df_anio_seleccionado['clas_con_f_alarma'].value_counts().reset_index()
            freq_alarma.columns = ['Alarma', 'Frecuencia']
            st.subheader(f"Frecuencia por alarma ({anio_seleccionado})")
            st.bar_chart(freq_alarma, x = 'Alarma', y = 'Frecuencia', x_label = 'Alarma', y_label = 'Frecuencia',
            horizontal = False)

Home()

#Mostrando el dataframe en una tabla
#st.dataframe(df_filter)