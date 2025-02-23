# Análisis Electoral Ecuador 2025 - Segunda Vuelta

## Descripción
Análisis y predicción de la segunda vuelta electoral en Ecuador 2025 usando datos oficiales del CNE.

## Estructura del Proyecto
- `data/raw/`: Datos crudos en formato JSON
- `data/processed/`: Datos procesados en CSV
- `notebooks/`: Análisis de datos y modelos predictivos
- `src/`: Scripts de extracción de datos

## Archivos Principales
- `src/script_provincia.py`: Script de web scraping
- `notebooks/AnalisisDatos.ipynb`: Análisis y modelado
- `data/processed/datos_elecciones_preparados.csv`: Datos preparados
- `data/processed/features_preparados.csv`: Features para modelado

## Uso
#### Requisitos Previos
- Python 3.9 o superior
- Google Chrome instalado
- ChromeDriver compatible con tu version de Chrome

#### Bibliotecas Python requeridas (instalar con pip):
- pip install selenium pandas numpy

#### Configuración Inicial
- Colocar el archivo `chromedriver.exe` en la ruta `"C:\Selenium\chromedriver.exe"`
- Asegurarse de tener acceso a internet y al sitio web del CNE

#### Extracción de Datos
Ejecutar el script:
- python script_provincia.py

El script iniciará un proceso interactivo donde:
1. Se abrirá automáticamente el navegador Chrome
2. Se cargará la página del CNE (elecciones2025.cne.gob.ec)
3. Se creará un directorio con timestamp para almacenar los resultados

Para cada provincia:
1. Seleccionar la provincia deseada del combobox
2. Presionar Enter en la consola
3. Esperar el mensaje de confirmación de extracción
4. Los datos se guardarán automáticamente

#### Los datos extraídos incluyen:
- Estadísticas generales (sufragantes, ausentismo, electores)
- Resultados por candidato
- Desglose de votos (válidos, blancos, nulos)

#### Archivos Generados
Para cada provincia se crean:
- `resultados_{provincia}.json`: Datos completos en formato JSON
- `estadisticas_{provincia}.csv`: Estadísticas generales
- `resultados_{provincia}.csv`: Resultados por candidato
- `votos_{provincia}.csv`: Desglose de tipos de votos

#### Finalización
- Presionar `Ctrl+C` para terminar la extracción
- El script cerrará automáticamente el navegador
- Los archivos quedarán guardados en la carpeta `resultados_elecciones_[timestamp]`

## Fuente de Datos
Consejo Nacional Electoral de Ecuador (CNE)