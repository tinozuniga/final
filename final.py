# Importar las librerías necesarias
import pandas as pd
import folium
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud
import plotly.express as px

# Configurar Matplotlib para que funcione bien con Streamlit
import matplotlib
matplotlib.use("Agg")

# Título llamativo con contexto inicial
st.title("🌐 Redes Sociales y Salud Mental: Un Análisis Interactivo 🧠")
st.write("""
Las redes sociales han revolucionado la forma en que nos conectamos con el mundo. Pero detrás de cada scroll infinito y cada like, surge una pregunta importante: ¿a qué precio?
En este blog interactivo, analizaremos el impacto del tiempo en línea en nuestra salud mental: desde las horas de sueño hasta los niveles de estrés y la productividad.
Acompáñanos a descubrir patrones, explorar datos y reflexionar sobre cómo equilibrar nuestra vida digital con nuestro bienestar. ¡Es hora de cuestionarnos nuestro tiempo en línea!
""")

# 🚀 Cargando las bases de datos
mental_health_file = "mental_health_and_technology_usage_2024.csv"
social_media_file = "social_media_usage.csv"
time_wasters_file = "Time-Wasters on Social Media.csv"

mental_health_df = pd.read_csv(mental_health_file)
social_media_df = pd.read_csv(social_media_file)
time_wasters_df = pd.read_csv(time_wasters_file)

### Limpieza de datos ###
# Convertir columnas clave a numérico para evitar problemas
for col in ['Age', 'Screen_Time_Hours', 'Sleep_Hours', 'Stress_Level']:
    mental_health_df[col] = pd.to_numeric(mental_health_df[col], errors='coerce')

# Limpiar filas con valores nulos
mental_health_df = mental_health_df.dropna(subset=['Age', 'Screen_Time_Hours', 'Sleep_Hours', 'Stress_Level'])

# Filtrar datos razonables (18-60 años)
mental_health_df = mental_health_df[(mental_health_df['Age'] >= 18) & (mental_health_df['Age'] <= 60)]

# Diagnóstico inicial (no se muestra en el blog, solo para verificar internamente)
diagnostic = mental_health_df.describe()

### 1. SALUD MENTAL Y TECNOLOGÍA ###
st.subheader("1. Explorando la relación entre salud mental y tecnología")

# Rango de edad interactivo
age_range = st.slider("Selecciona el rango de edad:", 18, 60, (18, 26))
mental_health_filtered = mental_health_df[
    (mental_health_df['Age'] >= age_range[0]) & (mental_health_df['Age'] <= age_range[1])
]

if not mental_health_filtered.empty:
    st.write("""
    #### ¿Qué buscamos responder?
    ¿Cómo afectan las horas frente a la pantalla nuestro sueño y estrés? Este gráfico muestra patrones según el rango de edad seleccionado.
    """)

    # Bubble Chart: Relación entre horas de pantalla, sueño y estrés
    bubble_chart = px.scatter(
        mental_health_filtered,
        x="Screen_Time_Hours",
        y="Sleep_Hours",
        size="Stress_Level",
        color="Mental_Health_Status",
        hover_name="Mental_Health_Status",
        title="Relación entre tiempo de pantalla, sueño y estrés"
    )
    st.plotly_chart(bubble_chart)

    st.write("Analicemos cómo el sueño varía según el estado de salud mental.")
    # Bar Chart: Promedio de sueño por estado mental
    bar_chart = px.bar(
        mental_health_filtered.groupby("Mental_Health_Status")["Sleep_Hours"].mean().reset_index(),
        x="Mental_Health_Status",
        y="Sleep_Hours",
        color="Mental_Health_Status",
        title="Horas promedio de sueño por estado de salud mental"
    )
    st.plotly_chart(bar_chart)

else:
    st.warning("No se encontraron datos para el rango seleccionado. Prueba otro rango.")

### 2. USO DE REDES SOCIALES ###
st.subheader("2. Análisis de las plataformas más populares")

# Selector interactivo para elegir análisis
social_analysis_type = st.selectbox(
    "Selecciona el análisis que deseas realizar:",
    ["Aplicaciones más usadas", "Frecuencia por aplicación", "Likes promedio por aplicación", "Distribución de likes"]
)

if social_analysis_type == "Aplicaciones más usadas":
    st.write("Visualizando las aplicaciones más populares con una nube de palabras.")
    text_apps = " ".join(social_media_df['App'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_apps)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

elif social_analysis_type == "Frecuencia por aplicación":
    st.write("Descubre qué aplicaciones son las más usadas.")
    app_frequencies = social_media_df['App'].value_counts()
    horizontal_bar_chart = px.bar(
        app_frequencies,
        orientation="h",  # Horizontal Bar Chart
        title="Frecuencia de uso por aplicación",
        labels={"value": "Frecuencia", "index": "Aplicación"}
    )
    st.plotly_chart(horizontal_bar_chart)

elif social_analysis_type == "Likes promedio por aplicación":
    st.write("¿Qué aplicaciones generan más likes? Aquí está la respuesta.")
    likes_by_app = social_media_df.groupby("App")["Likes_Per_Day"].mean().sort_values(ascending=False)
    bar_chart = px.bar(
        likes_by_app,
        title="Likes promedio por aplicación",
        labels={"value": "Likes Promedio", "index": "Aplicación"}
    )
    st.plotly_chart(bar_chart)

elif social_analysis_type == "Distribución de likes":
    st.write("Analizamos cómo se distribuyen los likes por día.")
    distplot = px.histogram(
        social_media_df,
        x="Likes_Per_Day",
        nbins=30,
        title="Distribución de likes diarios",
        labels={"Likes_Per_Day": "Likes por día"}
    )
    
    # Agregar borde a las barras del histograma
    distplot.update_traces(
        marker_line_width=1.5,  # Grosor del borde
        marker_line_color="black"  # Color del borde
    )
    
    st.plotly_chart(distplot)


### 3. TIEMPO DESPERDICIADO EN REDES SOCIALES ###
st.subheader("3. Plataformas y productividad")

st.write("""
#### Reflexión
¿Cuáles son las plataformas donde más tiempo gastamos? Este análisis busca responder cómo eso impacta nuestra productividad.
""")

# Sunburst Chart: Adicción según plataforma y tipo de dispositivo
st.write("Exploremos la adicción según plataforma y dispositivo.")

# Definir un mapa de colores específico
color_map = {
    "Bajo": "#6A0DAD",       # Morado
    "Moderado": "#FFA500",   # Naranja
    "Alto": "#FFFF00"        # Amarillo
}

sunburst_chart = px.sunburst(
    time_wasters_df,
    path=["Platform", "DeviceType"],
    values="Addiction Level",
    color="Addiction Level",
    color_discrete_map=color_map,  # Asignar colores personalizados
    title="Adicción por plataforma y tipo de dispositivo"
)

st.plotly_chart(sunburst_chart)


# Gráfico de barras: Tiempo promedio perdido por plataforma
platform_time = time_wasters_df.groupby("Platform")["Total Time Spent"].mean()

# Crear gráfico de barras con bordes y diseño atractivo
bar_chart = px.bar(
    platform_time,
    title="Tiempo promedio perdido por plataforma",
    labels={"value": "Tiempo Promedio (minutos)", "index": "Plataforma"},
    text=platform_time.round(2)  # Mostrar valores sobre las barras
)

# Personalización del gráfico
bar_chart.update_traces(
    marker_line_width=1.5,  # Grosor del borde
    marker_line_color="black",  # Color del borde
    textposition='outside'  # Ubicación de las etiquetas
)

bar_chart.update_layout(
    xaxis_title="Plataforma",
    yaxis_title="Tiempo Promedio (minutos)",
    title_x=0.5  # Centrar el título
)

# Mostrar gráfico en Streamlit
st.plotly_chart(bar_chart)
st.write("""
En esta gráfica se analiza el tiempo promedio que los usuarios dedican a diferentes plataformas digitales. Cada barra representa una plataforma y la cantidad de minutos que, en promedio, las personas pasan en ella cada día. Observamos cómo ciertas plataformas, como Instagram y TikTok, pueden absorber una gran parte de nuestro tiempo, mientras que otras, como LinkedIn, tienen un impacto más limitado. Este análisis permite identificar cuáles son las plataformas que más contribuyen al uso excesivo y podrían estar influyendo negativamente en nuestra productividad y bienestar.
""")




### Reflexión final ###
st.subheader("Conclusión")
st.write("""
Las redes sociales se han convertido en una parte fundamental de nuestra vida diaria, conectándonos con amigos, familiares y el mundo en general. Sin embargo, este análisis revela un impacto significativo en nuestra salud mental y productividad. Los datos muestran que plataformas como Instagram, TikTok y Facebook consumen gran parte de nuestro tiempo diario, lo que puede generar efectos secundarios como reducción en las horas de sueño, aumento de los niveles de estrés y menor productividad.

Por un lado, el uso excesivo de redes sociales puede llevar a una dependencia que afecta nuestra capacidad para concentrarnos en tareas importantes, además de influir en nuestra percepción de la realidad al exponernos constantemente a estándares poco realistas de éxito, belleza o estilo de vida. Por otro lado, no todas las plataformas tienen el mismo impacto. Por ejemplo, redes como LinkedIn se perciben más funcionales en términos de productividad, mientras que otras se asocian más con el ocio.

Este análisis también resalta que las horas frente a la pantalla están directamente relacionadas con las horas de sueño y, en algunos casos, con estados emocionales negativos. Los datos evidencian que debemos reflexionar sobre cómo usamos nuestro tiempo en línea y establecer límites saludables. Esto no significa eliminar las redes sociales, sino integrarlas de manera más consciente en nuestra rutina diaria.

En última instancia, el cambio está en nuestras manos. Podemos optar por establecer horarios específicos para el uso de redes, priorizar plataformas que agreguen valor a nuestra vida y desconectarnos cuando sea necesario. Más allá de los números, este análisis nos invita a tomar decisiones que nos permitan disfrutar de una vida digital equilibrada y saludable. 
""")


# Reflexión final
st.subheader("Conclusión")
st.write("""
Las redes sociales nos conectan, pero también tienen un impacto profundo en nuestra salud mental y productividad.  
Este análisis muestra datos para reflexionar: ¿cómo manejamos nuestro tiempo en línea?  
El cambio está en tus manos.  
""")

# Añadir imagen al final
st.image("foto.webp", caption="Una reflexión sobre nuestro tiempo en el mundo digital.", use_column_width=True)

