# --- 1. Librerías ---
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Rectangle, Circle
import matplotlib.patheffects as path_effects
from math import pi

# Configuración general - Usamos una fuente estándar disponible
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'  # Cambiamos a una fuente genérica

# --- 2. Datasets ---

# Dataset para el gráfico comparativo (del cell_id: fDUwqZZoPQKV)
data_comparativo = {
    "Métrica": ["Posesión (%)", "Tiros totales", "Tiros al arco", "xG", "Pases completados (%)", "Goles"],
    "Man. City": [74, 23, 8, 2.18, 92, 2],
    "Napoli": [26, 1, 1, 0.17, 79, 0]
}
df_comparativo = pd.DataFrame(data_comparativo)

# Dataset para el radar (del cell_id: HdTschBkPtHx)
metrics_radar = ["Posesión (%)", "Tiros totales", "Tiros al arco", "xG", "Pases completados (%)", "Goles"]
city_radar = [74, 23, 8, 2.18, 92, 2]
napoli_radar = [26, 1, 1, 0.17, 79, 0]
max_values_radar = [100, 30, 10, 3, 100, 5]
city_norm = [c/m*100 for c,m in zip(city_radar, max_values_radar)]
napoli_norm = [n/m*100 for n,m in zip(napoli_radar, max_values_radar)]

# Dataset para el timeline (del cell_id: fDUwqZZoPQKV y bsNV1TiMQQJP)
eventos_timeline = [
    {"minuto": 21, "equipo": "Napoli", "evento": "Expulsión Di Lorenzo", "color": "red"},
    {"minuto": 56, "equipo": "Man. City", "evento": "Gol Haaland", "color": "blue"},
    {"minuto": 65, "equipo": "Man. City", "evento": "Gol Doku", "color": "blue"},
]

# Dataset para análisis antes y después de expulsión (del cell_id: ViKgwKUyR_Q2)
data_fases = {
    "Fase": ["0-21' (11 vs 11)", "21'-90' (10 vs 11)"],
    "Posesión City (%)": [65, 76],
    "Posesión Napoli (%)": [35, 24],
    "Tiros City": [5, 18],
    "Tiros Napoli": [0, 1],
    "xG City": [0.6, 1.58],
    "xG Napoli": [0.1, 0.07]
}
df_fases = pd.DataFrame(data_fases)

# Datos simulados de xG acumulado (del cell_id: fSrzKSdESU2r y LlcdIIQdTk67)
minutos_xg = np.arange(0, 91, 5)
xg_city_acumulado = [0.1, 0.2, 0.3, 0.5, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.18, 2.18, 2.18, 2.18, 2.18, 2.18, 2.18]
xg_napoli_real_acumulado = [0.05, 0.08, 0.1, 0.1, 0.1, 0.11, 0.12, 0.13, 0.15, 0.16, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17]
xg_napoli_contrafactual_acumulado = np.linspace(0.05, 0.6, len(minutos_xg))
df_xg_acumulado = pd.DataFrame({
    "Minuto": minutos_xg,
    "xG_City": xg_city_acumulado,
    "xG_Napoli_Real": xg_napoli_real_acumulado,
    "xG_Napoli_11v11": xg_napoli_contrafactual_acumulado
})

# Datos para el mapa de calor (del cell_id: PxRPFYKwWNQK)
np.random.seed(42)
city_chances = {
    'x': np.concatenate([np.random.normal(70, 10, 15), np.random.normal(30, 5, 5)]),
    'y': np.concatenate([np.random.normal(50, 20, 15), np.random.normal(50, 10, 5)]),
    'valor': np.concatenate([np.random.uniform(0.1, 0.8, 15), np.random.uniform(0.05, 0.2, 5)])
}
napoli_chances = {
    'x': np.concatenate([np.random.normal(30, 10, 8), np.random.normal(70, 5, 2)]),
    'y': np.concatenate([np.random.normal(50, 15, 8), np.random.normal(50, 10, 2)]),
    'valor': np.concatenate([np.random.uniform(0.05, 0.4, 8), np.random.uniform(0.1, 0.3, 2)])
}

# Datos para la comparación de estadísticas (del cell_id: PxRPFYKwWNQK)
categories_stats = ['Tiros', 'Tiros a puerta', 'Posesión', 'Corners', 'Faltas']
city_stats = [18, 8, 68, 7, 12]
napoli_stats = [5, 1, 32, 2, 14]

# Datos para la distribución de xG por jugador (del cell_id: PxRPFYKwWNQK)
city_players = ['Haaland', 'Álvarez', 'Foden', 'Doku', 'Silva']
city_xg_players = [0.85, 0.45, 0.38, 0.25, 0.25]
napoli_players = ['Osimhen', 'Kvaratskhelia', 'Politano']
napoli_xg_players = [0.09, 0.05, 0.03]
players_xg = city_players + napoli_players
xg_values_players = city_xg_players + napoli_xg_players
colors_players = ['#1C3F95'] * len(city_players) + ['#9A1B1D'] * len(napoli_players)

# Datos para la evolución de la posesión (del cell_id: PxRPFYKwWNQK - Gráfico adicional)
segmentos_posesion = ['0-20', '21-45', '46-70', '71-90']
posesion_city_evolucion = [55, 75, 70, 72]
posesion_napoli_evolucion = [45, 25, 30, 28]


# --- 3. Funciones de visualización ---

# Función para dibujar el campo de fútbol (del cell_id: PxRPFYKwWNQK)
def draw_pitch(ax):
    pitch_length = 100
    pitch_width = 100
    ax.set_facecolor('#74a882')
    ax.plot([0, 0], [0, pitch_width], color='white', linewidth=2)
    ax.plot([0, pitch_length], [pitch_width, pitch_width], color='white', linewidth=2)
    ax.plot([pitch_length, pitch_length], [pitch_width, 0], color='white', linewidth=2)
    ax.plot([pitch_length, 0], [0, 0], color='white', linewidth=2)
    ax.plot([pitch_length/2, pitch_length/2], [0, pitch_width], color='white', linewidth=2)
    center_circle = plt.Circle((pitch_length/2, pitch_width/2), 10, color='white', fill=False, linewidth=2)
    ax.add_patch(center_circle)
    ax.scatter(pitch_length/2, pitch_width/2, color='white', s=20)
    ax.plot([0, 18], [pitch_width/2-10, pitch_width/2-10], color='white', linewidth=2)
    ax.plot([0, 18], [pitch_width/2+10, pitch_width/2+10], color='white', linewidth=2)
    ax.plot([18, 18], [pitch_width/2-10, pitch_width/2+10], color='white', linewidth=2)
    ax.plot([pitch_length, pitch_length-18], [pitch_width/2-10, pitch_width/2-10], color='white', linewidth=2)
    ax.plot([pitch_length, pitch_length-18], [pitch_width/2+10, pitch_width/2+10], color='white', linewidth=2)
    ax.plot([pitch_length-18, pitch_length-18], [pitch_width/2-10, pitch_width/2+10], color='white', linewidth=2)
    ax.plot([0, 30], [pitch_width/2-22, pitch_width/2-22], color='white', linewidth=2)
    ax.plot([0, 30], [pitch_width/2+22, pitch_width/2+22], color='white', linewidth=2)
    ax.plot([30, 30], [pitch_width/2-22, pitch_width/2+22], color='white', linewidth=2)
    ax.plot([pitch_length, pitch_length-30], [pitch_width/2-22, pitch_width/2-22], color='white', linewidth=2)
    ax.plot([pitch_length, pitch_length-30], [pitch_width/2+22, pitch_width/2+22], color='white', linewidth=2)
    ax.plot([pitch_length-30, pitch_length-30], [pitch_width/2-22, pitch_width/2+22], color='white', linewidth=2)
    ax.scatter(12, pitch_width/2, color='white', s=20)
    ax.scatter(pitch_length-12, pitch_width/2, color='white', s=20)
    ax.set_xlim(-5, pitch_length+5)
    ax.set_ylim(-5, pitch_width+5)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax

# --- 4. Generación de gráficos ---

# Gráfico comparativo de barras
df_comparativo_plot = df_comparativo.set_index("Métrica")
df_comparativo_plot.plot(kind="bar", figsize=(10,6))
plt.title("Manchester City vs Napoli - Champions League 2025")
plt.ylabel("Valor")
plt.xticks(rotation=45)
plt.legend(title="Equipo")
plt.show()

# Gráfico de radar
angles_radar = np.linspace(0, 2*np.pi, len(metrics_radar), endpoint=False).tolist()
city_norm_closed = city_norm + city_norm[:1]
napoli_norm_closed = napoli_norm + napoli_norm[:1]
angles_radar_closed = angles_radar + angles_radar[:1]

fig_radar, ax_radar = plt.subplots(figsize=(7,7), subplot_kw=dict(polar=True))
ax_radar.plot(angles_radar_closed, city_norm_closed, color="blue", linewidth=2, label="Man. City")
ax_radar.fill(angles_radar_closed, city_norm_closed, color="blue", alpha=0.25)
ax_radar.plot(angles_radar_closed, napoli_norm_closed, color="red", linewidth=2, label="Napoli")
ax_radar.fill(angles_radar_closed, napoli_norm_closed, color="red", alpha=0.25)
ax_radar.set_xticks(angles_radar[:-1])
ax_radar.set_xticklabels(metrics_radar, fontsize=10)
ax_radar.set_yticks([20,40,60,80,100])
ax_radar.set_yticklabels(["20","40","60","80","100"])
ax_radar.set_title("Manchester City vs Napoli - Radar Chart", size=14, weight="bold", pad=20)
ax_radar.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
plt.show()

# Timeline de eventos clave
fig_timeline, ax_timeline = plt.subplots(figsize=(10,2))
ax_timeline.hlines(1, 0, 90, color="gray", linewidth=1, alpha=0.7)
ax_timeline.set_xlim(0, 90)
ax_timeline.set_ylim(0.5, 1.5)
for ev in eventos_timeline:
    ax_timeline.scatter(ev["minuto"], 1, color=ev["color"], s=150, zorder=3)
    ax_timeline.text(ev["minuto"], 1.1, f"{ev['minuto']}' - {ev['evento']}",
            ha="center", va="bottom", fontsize=9, rotation=45)
ax_timeline.set_title("Manchester City vs Napoli - Línea de Tiempo de Eventos", fontsize=14, weight="bold", pad=20)
ax_timeline.axis("off")
plt.show()

# Visualización de posesión antes y después de la expulsión
df_pos_fases = df_fases[["Fase", "Posesión City (%)", "Posesión Napoli (%)"]].set_index("Fase")
df_pos_fases.plot(kind="bar", figsize=(8,5))
plt.title("Posesión antes y después de la expulsión")
plt.ylabel("% de posesión")
plt.xticks(rotation=0)
plt.show()

# Visualización de xG antes y después de la expulsión
df_xg_fases = df_fases[["Fase", "xG City", "xG Napoli"]].set_index("Fase")
df_xg_fases.plot(kind="bar", figsize=(8,5), color=["blue","red"])
plt.title("Expected Goals (xG) antes y después de la expulsión")
plt.ylabel("xG acumulado")
plt.xticks(rotation=0)
plt.show()

# Visualización de tiros antes y después de la expulsión
df_tiros_fases = df_fases[["Fase", "Tiros City", "Tiros Napoli"]].set_index("Fase")
df_tiros_fases.plot(kind="bar", figsize=(8,5), color=["blue","red"])
plt.title("Tiros antes y después de la expulsión")
plt.ylabel("Número de tiros")
plt.xticks(rotation=0)
plt.show()

# Curva de xG acumulado
plt.figure(figsize=(10,6))
plt.plot(df_xg_acumulado["Minuto"], df_xg_acumulado["xG_City"], label="Man. City", color="blue", linewidth=2)
plt.plot(df_xg_acumulado["Minuto"], df_xg_acumulado["xG_Napoli_Real"], label="Napoli (real, 10 vs 11)", color="red", linestyle="--", linewidth=2)
plt.plot(df_xg_acumulado["Minuto"], df_xg_acumulado["xG_Napoli_11v11"], label="Napoli (simulado, 11 vs 11)", color="green", linestyle=":", linewidth=2)
plt.axvline(x=21, color="black", linestyle="--", alpha=0.7)
plt.text(22, 0.05, "Expulsión 21'", fontsize=9, color="black")
plt.title("Curva de xG acumulado - Manchester City vs Napoli", fontsize=14, weight="bold")
plt.xlabel("Minuto de partido")
plt.ylabel("xG acumulado")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# Gráfico de barras comparativo de xG total
plt.figure(figsize=(8, 5))
categorias_xg_total = ['Man. City', 'Napoli (Real)', 'Napoli (11 vs 11)']
valores_xg_total = [df_xg_acumulado['xG_City'].iloc[-1], df_xg_acumulado['xG_Napoli_Real'].iloc[-1], df_xg_acumulado['xG_Napoli_11v11'].iloc[-1]]
colores_xg_total = ['blue', 'red', 'green']
plt.bar(categorias_xg_total, valores_xg_total, color=colores_xg_total, alpha=0.7)
plt.title('Comparación de xG Total', fontsize=14, weight='bold')
plt.ylabel('xG Total')
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(valores_xg_total):
    plt.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', weight='bold')
plt.show()

# Gráfico de diferencia de xG por segmentos del partido
plt.figure(figsize=(10, 6))
minuto_expulsion = 21
segmento_pre = df_xg_acumulado[df_xg_acumulado['Minuto'] <= minuto_expulsion]
segmento_post = df_xg_acumulado[df_xg_acumulado['Minuto'] > minuto_expulsion]
plt.bar(segmento_pre['Minuto'], segmento_pre['xG_City'] - segmento_pre['xG_Napoli_Real'],
        width=4, alpha=0.7, label='Pre-expulsión', color='lightblue')
plt.bar(segmento_post['Minuto'], segmento_post['xG_City'] - segmento_post['xG_Napoli_Real'],
        width=4, alpha=0.7, label='Post-expulsión', color='darkblue')
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.axvline(x=minuto_expulsion, color='red', linestyle='--', alpha=0.7)
plt.text(minuto_expulsion + 2, 1.8, 'Expulsión', fontsize=10, color='red')
plt.title('Diferencia de xG (City - Napoli) por segmentos del partido', fontsize=14, weight='bold')
plt.xlabel('Minuto de partido')
plt.ylabel('Diferencia de xG')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# Gráfico de radar para comparación múltiple
categorias_radar_multiple = ['xG Total', 'xG Post-Expulsión', 'Dominio Ofensivo', 'Eficacia']
valores_city_multiple = [2.18, 1.58, 9, 8]
valores_napoli_real_multiple = [0.17, 0.02, 3, 4]
valores_napoli_11v11_multiple = [0.60, 0.45, 7, 6]
valores_city_multiple += valores_city_multiple[:1]
valores_napoli_real_multiple += valores_napoli_real_multiple[:1]
valores_napoli_11v11_multiple += valores_napoli_11v11_multiple[:1]
categorias_radar_multiple += categorias_radar_multiple[:1]
fig_radar_multiple, ax_radar_multiple = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
angles_radar_multiple = [n / float(len(categorias_radar_multiple) - 1) * 2 * pi for n in range(len(categorias_radar_multiple))]
ax_radar_multiple.plot(angles_radar_multiple, valores_city_multiple, 'o-', linewidth=2, label='Man. City', color='blue')
ax_radar_multiple.fill(angles_radar_multiple, valores_city_multiple, alpha=0.25, color='blue')
ax_radar_multiple.plot(angles_radar_multiple, valores_napoli_real_multiple, 'o-', linewidth=2, label='Napoli (Real)', color='red')
ax_radar_multiple.fill(angles_radar_multiple, valores_napoli_real_multiple, alpha=0.25, color='red')
ax_radar_multiple.plot(angles_radar_multiple, valores_napoli_11v11_multiple, 'o-', linewidth=2, label='Napoli (11v11)', color='green')
ax_radar_multiple.fill(angles_radar_multiple, valores_napoli_11v11_multiple, alpha=0.25, color='green')
ax_radar_multiple.set_xticks(angles_radar_multiple[:-1])
ax_radar_multiple.set_xticklabels(categorias_radar_multiple[:-1])
ax_radar_multiple.set_yticklabels([])
ax_radar_multiple.set_title('Comparación de Rendimiento - Análisis Multidimensional', size=14, weight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.show()

# Creación del dashboard principal
fig_dashboard = plt.figure(figsize=(15, 12))
fig_dashboard.patch.set_facecolor('#f0f0f0')
plt.suptitle('Análisis Manchester City vs Napoli - Champions League',
             fontsize=18, fontweight='bold', y=0.97)

# Gráfico 1: Mapa de calor de oportunidades
ax1_dashboard = plt.subplot2grid((3, 2), (0, 0), colspan=1)
draw_pitch(ax1_dashboard)
sc1_dashboard = ax1_dashboard.scatter(city_chances['x'], city_chances['y'],
                 c=city_chances['valor'], cmap='Blues',
                 s=city_chances['valor']*100, alpha=0.7, label='Man City')
sc2_dashboard = ax1_dashboard.scatter(napoli_chances['x'], napoli_chances['y'],
                 c=napoli_chances['valor'], cmap='Reds',
                 s=napoli_chances['valor']*100, alpha=0.7, label='Napoli')
cbar_dashboard = plt.colorbar(sc1_dashboard, ax=ax1_dashboard, shrink=0.6)
cbar_dashboard.set_label('Valor de oportunidad (xG)', fontsize=10)
ax1_dashboard.set_title('Mapa de calor de oportunidades de gol', fontweight='bold')
ax1_dashboard.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)

# Gráfico 2: xG acumulado en el dashboard
ax2_dashboard = plt.subplot2grid((3, 2), (0, 1), colspan=1)
ax2_dashboard.plot(minutos_xg, xg_city_acumulado, label="Man. City", color="#1C3F95", linewidth=2.5)
ax2_dashboard.plot(minutos_xg, xg_napoli_real_acumulado, label="Napoli (real, 10 vs 11)", color="#9A1B1D", linestyle="--", linewidth=2.5)
ax2_dashboard.plot(minutos_xg, xg_napoli_contrafactual_acumulado, label="Napoli (simulado, 11 vs 11)", color="#009246", linestyle=":", linewidth=2.5)
ax2_dashboard.axvline(x=21, color="black", linestyle="--", alpha=0.7)
ax2_dashboard.text(22, 0.1, "Expulsión 21'", fontsize=10, color="black", fontweight='bold')
ax2_dashboard.set_title("Curva de xG acumulado", fontsize=14, weight="bold")
ax2_dashboard.set_xlabel("Minuto de partido")
ax2_dashboard.set_ylabel("xG acumulado")
ax2_dashboard.legend()
ax2_dashboard.grid(alpha=0.3)
ax2_dashboard.set_xlim(0, 90)

# Gráfico 3: Comparación de estadísticas en el dashboard
ax3_dashboard = plt.subplot2grid((3, 2), (1, 0), colspan=2)
x_stats = np.arange(len(categories_stats))
width_stats = 0.35
bars1_stats = ax3_dashboard.bar(x_stats - width_stats/2, city_stats, width_stats, label='Man City', color='#1C3F95', alpha=0.8)
bars2_stats = ax3_dashboard.bar(x_stats + width_stats/2, napoli_stats, width_stats, label='Napoli', color='#9A1B1D', alpha=0.8)
ax3_dashboard.set_ylabel('Cantidad / Porcentaje')
ax3_dashboard.set_title('Comparación de estadísticas del partido', fontweight='bold')
ax3_dashboard.set_xticks(x_stats)
ax3_dashboard.set_xticklabels(categories_stats)
ax3_dashboard.legend()
for bar in bars1_stats:
    height = bar.get_height()
    ax3_dashboard.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold')
for bar in bars2_stats:
    height = bar.get_height()
    ax3_dashboard.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold')
ax3_dashboard.grid(axis='y', alpha=0.3)

# Gráfico 4: Distribución de xG por jugador en el dashboard
ax4_dashboard = plt.subplot2grid((3, 2), (2, 0), colspan=2)
bars_players = ax4_dashboard.barh(players_xg, xg_values_players, color=colors_players, alpha=0.8)
ax4_dashboard.set_xlabel('xG Total')
ax4_dashboard.set_title('Distribución de xG por jugador', fontweight='bold')
ax4_dashboard.grid(axis='x', alpha=0.3)
for bar in bars_players:
    width = bar.get_width()
    ax4_dashboard.text(width + 0.01, bar.get_y() + bar.get_height()/2,
             f'{width:.2f}', ha='left', va='center', fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.96])
fig_dashboard.text(0.05, 0.02,
         "Análisis táctico: El Manchester City dominó claramente el partido tras la expulsión en el minuto 21.\n"
         "El mapa de calor muestra la superioridad ofensiva del City, con la mayoría de oportunidades creadas en campo rival.",
         fontsize=10, style='italic', color='#555555')
plt.show()

# Gráfico adicional: Evolución de la posesión
fig_posesion_evolucion, ax5_posesion_evolucion = plt.subplots(figsize=(10, 4))
ax5_posesion_evolucion.plot(segmentos_posesion, posesion_city_evolucion, marker='o', label='Man City', color='#1C3F95', linewidth=2)
ax5_posesion_evolucion.plot(segmentos_posesion, posesion_napoli_evolucion, marker='o', label='Napoli', color='#9A1B1D', linewidth=2)
ax5_posesion_evolucion.set_ylabel('Posesión (%)')
ax5_posesion_evolucion.set_xlabel('Segmento del partido')
ax5_posesion_evolucion.set_title('Evolución de la posesión por segmentos', fontweight='bold')
ax5_posesion_evolucion.legend()
ax5_posesion_evolucion.grid(alpha=0.3)
for i, v in enumerate(posesion_city_evolucion):
    ax5_posesion_evolucion.text(i, v + 1, f'{v}%', ha='center', va='bottom', fontweight='bold')
for i, v in enumerate(posesion_napoli_evolucion):
    ax5_posesion_evolucion.text(i, v - 2, f'{v}%', ha='center', va='top', fontweight='bold')
plt.tight_layout()
plt.show()
