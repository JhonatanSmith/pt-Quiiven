# Prueba tecnica

Este repositorio contiene el desarrollo de un caso práctico para segmentacion de clientes inmobiliarios

---

## Estructura del proyecto

```text
├── data/              # Datos entregados
│
├── docs/              # Documentación del caso entregada por la empresa
│
├── notebooks/         # Exploración y modelado en Jupyter (EDA, segmentación, reglas)
│
├── results/           # Resultados del modelo entrenado y visualizaciones
│   ├── models/        # Modelo entrenado
│   └── pics/          # Gráficos generados durante el análisis y visualización
│
├── scripts/           # Scripts Python que ejecutan cada etapa del pipeline
│   ├── data_silver.py # Limpieza y consolidación de datos
│   ├── data_gold.py   # Agregación y feature engineering
│   ├── model.py       # Entrenamiento del modelo de clustering
│   └── utils.py       # Funciones auxiliares reutilizables
│
├── main.py            # Script principal (Ideal para orquestacion, app de Streamlit)
├── requirements.txt   # Dependencias del proyecto
├── .gitignore         # Exclusiones para Git
```
---
# Notas adicionales

 * El proyecto puede escalar a clustering jerárquico o modelos supervisados si se incorporan etiquetas.
 * Las visualizaciones clave están disponibles en results/pics/.
 * El enlace para la expo de Google Slide se encuentra [aqui](https://docs.google.com/presentation/d/e/2PACX-1vQ8LdfHeBDI6vQxf6fhMiivevOZjTZlGLVUwc0MHmZVm0QolUolfb2JEiITTgGY5BjUPaQSLHDSpLs6/pub?start=false&loop=false&delayms=60000)


