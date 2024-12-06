# Importar librerías necesarias
import pandas as pd
import folium
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud

# Configurar el backend de Matplotlib para Streamlit
import matplotlib
matplotlib.use("Agg")

# Iniciar la aplicación
st.title("Análisis de Datos sobre Redes Sociales y Tecnología")
st.write("Este blog interactivo analiza el impacto de las redes sociales y el uso de tecnología en la salud mental.")

# Archivos CSV (deben estar en la misma carpeta que el script)
mental_health_file = "mental_health_and_technology_usage_2024.csv"
social_media_file = "social_media_usage.csv"
time_wasters_file = "Time-Wasters on Social Media.csv"

# Cargar las bases de datos
mental_health_df = pd.read_csv(mental_health_file)
social_media_df = pd.read_csv(social_media_file)
time_wasters_df = pd.read_csv(time_wasters_file)

# 1. Primera Base de Datos: Salud Mental y Tecnología
st.subheader("1. Análisis de Salud Mental y Tecnología")

# Filtrar edades entre 18 y 26 años
mental_health_filtered = mental_health_df[(mental_health_df['Age'] >= 18) & (mental_health_df['Age'] <= 26)]

# Gráfica 1: Promedio de Uso de Redes Sociales por Edad
average_usage_by_age = mental_health_filtered.groupby('Age')['Social_Media_Usage_Hours'].mean()
plt.figure()
plt.plot(average_usage_by_age.index, average_usage_by_age.values, marker='o', linestyle='-')
plt.xlabel('Edad (Años)')
plt.ylabel('Promedio de Horas de Uso de Redes Sociales')
plt.title('Promedio de Uso de Redes Sociales por Edad')
plt.grid(True)
st.pyplot(plt)

# Gráfica 2: Horas Promedio de Uso de Redes Sociales por Estado de Salud Mental
average_usage_by_health_status = mental_health_filtered.groupby('Mental_Health_Status')['Social_Media_Usage_Hours'].mean()
plt.figure()
average_usage_by_health_status.plot(kind='barh', color='brown')
plt.xlabel('Promedio de Horas de Uso de Redes Sociales')
plt.ylabel('Estado de Salud Mental')
plt.title('Horas Promedio de Uso de Redes Sociales por Estado de Salud Mental')
plt.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(plt)

# Gráfica 3: Promedio de Horas de Sueño por Intervalo de Tiempo en Pantalla
bins = [0, 2, 4, 6, 8, 10, 12, 14, 16]
labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins) - 1)]
mental_health_filtered['Screen_Time_Range'] = pd.cut(mental_health_filtered['Screen_Time_Hours'], bins=bins, labels=labels, include_lowest=True)
average_sleep_by_screen_time = mental_health_filtered.groupby('Screen_Time_Range')['Sleep_Hours'].mean()
plt.figure()
average_sleep_by_screen_time.plot(kind='bar', color='purple', edgecolor='green', alpha=0.5)
plt.xlabel('Intervalo de Horas de Tiempo en Pantalla')
plt.ylabel('Promedio de Horas de Sueño')
plt.title('Promedio de Horas de Sueño por Intervalo de Tiempo en Pantalla')
plt.grid(axis='y', linestyle='--', alpha=1)
plt.xticks(rotation=45)
st.pyplot(plt)

# 2. Segunda Base de Datos: Uso de Redes Sociales
st.subheader("2. Análisis de Uso de Redes Sociales")

# Gráfica 1: WordCloud de Aplicaciones Más Usadas
text_apps = " ".join(social_media_df['App'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_apps)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('WordCloud de Aplicaciones Más Usadas', fontsize=16)
st.pyplot(plt)

# Gráfica 2: Frecuencia de Uso por Aplicación
app_frequencies = social_media_df['App'].value_counts()
plt.figure(figsize=(12, 6))
app_frequencies.plot(kind='bar', color='skyblue', edgecolor='black', alpha=0.7)
plt.xlabel('Aplicación')
plt.ylabel('Frecuencia')
plt.title('Frecuencia de Uso por Aplicación')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

# Gráfica 3: Promedio de Horas Diarias Gastadas por Aplicación
average_hours_per_app = social_media_df.groupby('App')['Daily_Minutes_Spent'].mean() / 60
plt.figure(figsize=(12, 6))
average_hours_per_app.sort_values(ascending=False).plot(kind='bar', color='skyblue', edgecolor='black', alpha=0.7)
plt.ylim(3.5, 4.5)
plt.xlabel('Aplicación')
plt.ylabel('Promedio de Horas Diarias')
plt.title('Promedio de Horas Diarias Gastadas por Aplicación (Rango 3:30 a 4:30 horas)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

# Gráfica 4: Promedio de Likes Diarios por Aplicación
average_likes_per_app = social_media_df.groupby('App')['Likes_Per_Day'].mean()
plt.figure(figsize=(12, 6))
average_likes_per_app.sort_values(ascending=False).plot(kind='bar', color='skyblue', edgecolor='black', alpha=0.7)
plt.xlabel('Aplicación')
plt.ylabel('Promedio de Likes Diarios')
plt.title('Promedio de Likes Diarios por Aplicación')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

# 3. Tercera Base de Datos: Tiempo Desperdiciado en Redes Sociales
st.subheader("3. Análisis de Plataformas que Desperdician Tiempo")

# Gráfica 1: Nivel Promedio de Adicción por Plataforma
average_addiction_per_platform = time_wasters_df.groupby('Platform')['Addiction Level'].mean()
plt.figure(figsize=(12, 6))
average_addiction_per_platform.sort_values(ascending=False).plot(kind='barh', color='green', edgecolor='black', alpha=0.7)
plt.ylabel('Plataforma')
plt.xlabel('Nivel Promedio de Adicción')
plt.title('Nivel Promedio de Adicción por Plataforma')
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

# Gráfica 2: Tiempo Promedio Total Gastado por Plataforma
average_time_spent_per_platform = time_wasters_df.groupby('Platform')['Total Time Spent'].mean()
plt.figure(figsize=(12, 6))
average_time_spent_per_platform.sort_values(ascending=False).plot(kind='bar', color='skyblue', edgecolor='black', alpha=0.7)
plt.ylim(140, 160)
plt.xlabel('Plataforma')
plt.ylabel('Tiempo Promedio Total Gastado (Minutos)')
plt.title('Tiempo Promedio Total Gastado por Plataforma (140-160 minutos)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

# Mapa: Frecuencia de Usuarios por País
st.write("Mapa interactivo de ubicación de usuarios:")
location_counts = time_wasters_df['Location'].value_counts()
location_coordinates = {
    "United States": [37.0902, -95.7129],
    "India": [20.5937, 78.9629],
    "Brazil": [-14.2350, -51.9253],
    "Germany": [51.1657, 10.4515],
    "Japan": [36.2048, 138.2529],
    "Canada": [56.1304, -106.3468],
    "Australia": [-25.2744, 133.7751],
    "Vietnam": [21.0285, 105.8542],
    "Philippines": [14.5995, 120.9842],
    "Indonesia": [-6.2088, 106.8456],
    "Pakistan": [33.6844, 73.0479],
    "Mexico": [19.4326, -99.1332],
}
base_map = folium.Map(location=[0, 0], zoom_start=2)
for location, count in location_counts.items():
    if location in location_coordinates:
        folium.Marker(
            location=location_coordinates[location],
            popup=f"{location}: {count} usuarios"
        ).add_to(base_map)
st.components.v1.html(base_map._repr_html_(), height=500)
