# TP2 - Aproximación de imágenes con triángulos usando Algoritmos Genéticos

Este proyecto implementa un algoritmo genético para aproximar una imagen objetivo utilizando únicamente triángulos semitransparentes.

La idea general es representar cada solución candidata como una imagen compuesta por `N` triángulos, y hacer evolucionar una población de individuos para que la imagen generada se parezca cada vez más a la imagen objetivo.

---

## Objetivo

Dada una imagen de entrada, el algoritmo debe:

- generar una aproximación visual con triángulos,
- optimizar esa aproximación usando un algoritmo genético,
- devolver:
  - la mejor imagen encontrada,
  - la lista de triángulos del mejor individuo,
  - métricas de evolución del proceso.

---

## Representación del individuo

Cada triángulo se representa con 10 parámetros normalizados en `[0,1]`:

[x1, y1, x2, y2, x3, y3, r, g, b, a]

donde:

- `x1, y1, x2, y2, x3, y3` son las coordenadas de los 3 vértices
- `r, g, b` son los canales de color
- `a` es el alpha (transparencia)

Un individuo contiene una lista de `num_triangles` triángulos.

---

## Estructura general del proyecto

- `engine/`
  - `individual.py`  
    Representación de un individuo
  - `population.py`  
    Manejo de la población
  - `genetic_algorithm.py`  
    Motor principal del algoritmo genético

- `operators/`
  - `selection/`  
    Métodos de selección
  - `crossover/`  
    Métodos de cruce
  - `mutation/`  
    Métodos de mutación

- `replacement/`
  - Estrategias de supervivencia / reemplazo

- `rendering/`
  - `renderer.py`  
    Convierte un individuo en una imagen real

- `fitness/`
  - `image_fitness.py`  
    Compara la imagen generada con la imagen objetivo

- `metrics/`
  - `tracker.py`  
    Guarda la evolución de la fitness

- `stopping/`
  - `criteria.py`  
    Criterios de parada

- `utils/`
  - carga de configuración / utilidades auxiliares

- `test_main.py`
  - script principal para correr experimentos manuales

- `main.py`
  - punto de entrada del proyecto

---

## Renderizado

El renderizado se hace sobre un fondo blanco usando composición alpha real.

Eso significa que:

- el orden de los triángulos importa,
- la transparencia importa,
- la imagen final se construye superponiendo triángulos uno sobre otro.

---

## Fitness

La fitness compara la imagen generada con la imagen objetivo.

Actualmente, la versión recomendada combina:

- error de color RGB
- y opcionalmente error sobre bordes / contornos

La forma general es:

- `fitness = 1 - error`

Por lo tanto:

- fitness alta = mejor aproximación
- fitness baja = peor aproximación

---

## Inicialización disponible

### 1. `random`
Inicialización completamente aleatoria.

### 2. `guided`
Inicialización guiada por la imagen objetivo:
- toma colores desde la imagen objetivo,
- ubica triángulos alrededor de zonas reales de la imagen,
- mejora mucho el punto de partida del algoritmo.

---

## Métodos implementados

### Selección
- `elite`
- `roulette`
- `universal`
- `boltzmann`
- `tournament_deterministic`
- `tournament_probabilistic`
- `ranking`

### Crossover
- `one_point`
- `two_point`
- `uniform`
- `annular`

### Mutación
- `gen`
- `multigen`
- `non_uniform`

### Replacement
- `exclusive`
- `additive`

---

## Criterios de parada

El algoritmo puede detenerse por:

- cantidad máxima de generaciones,
- fitness objetivo alcanzada,
- demasiadas generaciones sin mejora.

---

## Métricas guardadas

Durante la ejecución se registran:

- mejor fitness
- fitness promedio
- peor fitness

Y se exportan como:

- `metrics.json`
- `fitness_plot.png`

---

## Archivos generados por cada ejecución

Cada run genera:

- `target.png`  
  imagen objetivo redimensionada
- `best.png`  
  mejor imagen encontrada
- `best_triangles.txt`  
  lista de triángulos del mejor individuo
- `metrics.json`  
  historial de métricas
- `fitness_plot.png`  
  gráfico de evolución de la fitness

---

## Ejemplo de ejecución

```bash
sh scripts/run_all.sh
```

---

## Resultados y Parámetros Recomendados

Tras ejecutar una automatización exhaustiva comparando combinaciones sistemáticas de algoritmos en múltiples semillas y configuraciones, se obtuvieron las siguientes conclusiones:

1. **Selección:** El Torneo Determinístico (`tournament_deterministic`) domina consistentemente sobre todos los demás métodos, probablemente porque mantiene una fuerte presión selectiva mientras preserva a los individuos de alta aptitud, lo que es crítico para el avance constante en un paisaje de aptitud tan amplio.
2. **Mutación:** La Mutación No Uniforme (`non_uniform`) lidera de forma decisiva las posiciones superiores en el ranking. Al explorar de forma mucho más amplia en etapas tempranas y acotar la variación en generaciones tardías, permite que los contornos y detalles de los triángulos encajen precisamente sobre los bordes detectados en la fitness.
3. **Crossover:** El Cruce Uniforme (`uniform`) presenta una ligera ventaja frente a `two_point` ya que dispersa mejor los canales de vértices evitando la rápida convergencia prematura local y proveyendo configuraciones de triángulos sumamente variadas a la descendencia.

### Configuración Ganadora
Basado en las estadísticas recolectadas, la configuración recomendada para optimizar la calidad de los polígonos bajo un esquema competitivo es:

```bash
python main.py \
  --image inputs/flags/fr.png \
  --population-size 100 \
  --triangles 50 \
  --generations 300 \
  --selection tournament_deterministic \
  --crossover uniform \
  --mutation non_uniform \
  --replacement exclusive
```

### Script de Experimentos Sistemáticos

El proyecto cuenta con un script capaz de automatizar las búsquedas:

```bash
python run_experiments.py \
  --image inputs/flags/fr.png \
  --output-dir outputs/experiments/fr \
  --image-size 64 \
  --population-size 100 \
  --triangles 40 \
  --generations 200 \
  --selection-methods tournament_deterministic,universal \
  --crossover-methods uniform,two_point \
  --mutation-methods multigen,non_uniform \
  --replacement-methods additive,exclusive \
  --repetitions 3
```
Esta ejecución probará todas las combinaciones (producto cartesiano) permitiendo analizar las correlaciones entre operadores en `outputs/experiments/fr/summary.json`.
