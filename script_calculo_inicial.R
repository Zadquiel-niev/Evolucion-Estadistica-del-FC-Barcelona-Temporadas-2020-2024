
library(dplyr)
library(ggplot2)
library(corrplot)
library(readr)
library(plotly)
library(patchwork)
matches_full_la_liga <-read_csv('matches_full_la_liga.csv')
# Filtrar datos del Barcelona
barca_data <- matches_full_la_liga %>% 
  filter(team == "Barcelona", season %in% c(2021, 2022, 2023, 2024, 2025))


tendencias_anuales <- barca_data %>%
  group_by(season) %>%
  summarise(
    partidos_jugados = n(),
    goles_favor = sum(gf, na.rm = TRUE),
    goles_contra = sum(ga, na.rm = TRUE),
    promedio_gf = mean(gf, na.rm = TRUE),
    promedio_ga = mean(ga, na.rm = TRUE),
    promedio_posesion = mean(poss, na.rm = TRUE),
    promedio_xg = mean(xg, na.rm = TRUE),
    promedio_xga = mean(xga, na.rm = TRUE),
    victorias = sum(result == "W", na.rm = TRUE),
    empates = sum(result == "D", na.rm = TRUE),
    derrotas = sum(result == "L", na.rm = TRUE),
    puntos = (victorias * 3) + empates
  ) %>%
  mutate(
    efectividad = (puntos / (partidos_jugados * 3)) * 100,
    diferencia_goles = goles_favor - goles_contra
  )

# Evolución ofensiva
evolucion_ofensiva <- barca_data %>%
  group_by(season) %>%
  summarise(
    tiros_por_partido = mean(sh, na.rm = TRUE),
    tiros_porteria_por_partido = mean(sot, na.rm = TRUE),
    efectividad_tiro = (sum(sot, na.rm = TRUE) / sum(sh, na.rm = TRUE)) * 100,
    conversion_goles = (sum(gf, na.rm = TRUE) / sum(sh, na.rm = TRUE)) * 100
  )


# Matriz de correlación general
correlacion_general <- barca_data %>%
  select(poss, xg, xga, gf, ga, sh, sot) %>%
  cor(use = "complete.obs")

# Correlación por temporada
correlacion_por_temporada <- barca_data %>%
  group_by(season) %>%
  summarise(
    cor_poss_xg = cor(poss, xg, use = "complete.obs"),
    cor_poss_xga = cor(poss, xga, use = "complete.obs"),
    cor_poss_gf = cor(poss, gf, use = "complete.obs"),
    cor_poss_puntos = cor(poss, 
                          ifelse(result == "W", 3, 
                                 ifelse(result == "D", 1, 0)), 
                          use = "complete.obs")
  )

# Eficiencia ofensiva vs posesión
eficiencia_posesion <- barca_data %>%
  mutate(
    categoria_posesion = cut(poss, 
                             breaks = c(0, 50, 60, 70, 100),
                             labels = c("Baja", "Media", "Alta", "Muy Alta"))
  ) %>%
  group_by(categoria_posesion) %>%
  summarise(
    partidos = n(),
    promedio_gf = mean(gf, na.rm = TRUE),
    promedio_xg = mean(xg, na.rm = TRUE),
    eficiencia_ataque = mean(gf / xg, na.rm = TRUE),
    puntos_por_partido = mean(ifelse(result == "W", 3, 
                                     ifelse(result == "D", 1, 0)), na.rm = TRUE)
  )


g1 <- ggplot(tendencias_anuales, aes(x = season)) +
  geom_line(aes(y = promedio_gf, color = "Goles a Favor"), size = 1.5) +
  geom_line(aes(y = promedio_ga, color = "Goles en Contra"), size = 1.5) +
  geom_point(aes(y = promedio_gf), size = 3, color = "#004D98") +
  geom_point(aes(y = promedio_ga), size = 3, color = "#A50044") +
  labs(title = "Evolución Ofensiva del FC Barcelona (2020-2024)",
       subtitle = "Promedio de Goles por Partido",
       x = "Temporada", y = "Goles por Partido",
       color = "Métrica") +
  scale_color_manual(values = c("Goles a Favor" = "#004D98", 
                                "Goles en Contra" = "#A50044")) +
  theme_minimal() +
  theme(legend.position = "bottom")

g2 <- ggplot(tendencias_anuales, aes(x = season)) +
  geom_col(aes(y = promedio_posesion, fill = promedio_posesion), alpha = 0.8) +
  geom_line(aes(y = efectividad, color = "Efectividad (%)"), size = 1.5, group = 1) +
  geom_point(aes(y = efectividad), size = 3, color = "#FFD700") +
  scale_y_continuous(sec.axis = sec_axis(~./1, name = "Efectividad (%)")) +
  labs(title = "Posesión y Efectividad por Temporada",
       x = "Temporada", y = "Posesión (%)") +
  scale_fill_gradient(low = "#87CEEB", high = "#004D98", name = "Posesión (%)") +
  scale_color_manual(values = c("Efectividad (%)" = "#FFD700")) +
  theme_minimal()
