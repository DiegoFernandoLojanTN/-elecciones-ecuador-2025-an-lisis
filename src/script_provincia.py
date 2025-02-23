import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from datetime import datetime

class EleccionesEcuadorManual:
    def __init__(self):
        self.url = "https://elecciones2025.cne.gob.ec"
        self.setup_driver()
        self.crear_directorios()

    def crear_directorios(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = f"resultados_elecciones_{timestamp}"
        os.makedirs(self.base_dir, exist_ok=True)

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(
            service=Service("C:\\Selenium\\chromedriver.exe"),
            options=chrome_options
        )

    def extraer_datos_actuales(self):
        try:
            # Esperar a que los elementos estén presentes
            time.sleep(3)

            # Obtener provincia actual
            provincia = self.driver.execute_script(
                "return $('#sbProvincia').dxSelectBox('instance').option('text');"
            )

            # Hacer clic en el botón Buscar usando el selector correcto
            buscar_button = self.driver.find_element(By.CSS_SELECTOR, "a.btn.btn-secondary")
            buscar_button.click()

            # Esperar a que se actualicen los datos
            time.sleep(3)

            # Extraer datos del gráfico de barras
            resultados_candidatos = self.driver.execute_script(
                "return $('#chart1').dxChart('instance').getDataSource().items();"
            )

            # Extraer estadísticas
            stats = {
                'provincia': provincia,
                'sufragantes': self.driver.find_element(By.ID, "Sufragantes").text,
                'ausentismo': self.driver.find_element(By.ID, "Ausentismo").text,
                'electores': self.driver.find_element(By.ID, "Electores").text
            }

            # Extraer datos de votos válidos, blancos y nulos
            votos_data = self.driver.execute_script(
                "return $('#pie').dxPieChart('instance').option('dataSource');"
            )

            datos_votos = []
            for item in votos_data:
                datos_votos.append({
                    'tipo': item['DESCRIPCION'],
                    'valor': item['VALOR']
                })

            # Guardar datos
            self.guardar_datos(provincia, stats, resultados_candidatos, datos_votos)

            print(f"\n¡Extracción completada para {provincia}!")
            print("Datos guardados en archivos JSON y CSV")
            print("\nPuedes seleccionar otra provincia y presionar Buscar...")

            return True

        except Exception as e:
            print(f"Error al extraer datos: {str(e)}")
            return False

    def guardar_datos(self, provincia, stats, resultados_candidatos, datos_votos):
        provincia_nombre = provincia.lower().replace(' ', '_')

        # Crear el objeto de datos completo
        datos_completos = {
            'estadisticas': stats,
            'resultados_candidatos': resultados_candidatos,
            'datos_votos': datos_votos
        }

        # Guardar JSON
        json_file = os.path.join(self.base_dir, f"resultados_{provincia_nombre}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(datos_completos, f, ensure_ascii=False, indent=4)

        # Guardar CSVs
        df_stats = pd.DataFrame([stats])
        df_resultados = pd.DataFrame(resultados_candidatos)
        df_votos = pd.DataFrame(datos_votos)

        csv_stats = os.path.join(self.base_dir, f"estadisticas_{provincia_nombre}.csv")
        csv_resultados = os.path.join(self.base_dir, f"resultados_{provincia_nombre}.csv")
        csv_votos = os.path.join(self.base_dir, f"votos_{provincia_nombre}.csv")

        df_stats.to_csv(csv_stats, index=False)
        df_resultados.to_csv(csv_resultados, index=False)
        df_votos.to_csv(csv_votos, index=False)

    def iniciar_extraccion_manual(self):
        self.driver.get(self.url)
        time.sleep(5)

        print("\n=== Extractor Manual de Resultados Electorales ===")
        print("\nInstrucciones:")
        print("1. Selecciona una provincia del combobox")
        print("2. Presiona Enter para extraer los datos")
        print("3. Espera el mensaje de confirmación")
        print("4. Repite el proceso para cada provincia")
        print("\nPresiona Ctrl+C cuando hayas terminado.")

        try:
            while True:
                input("\nPresiona Enter cuando hayas seleccionado una provincia...")
                self.extraer_datos_actuales()

        except KeyboardInterrupt:
            print("\n\nFinalizando extracción...")
            print(f"\nTodos los datos han sido guardados en: {self.base_dir}")

    def cerrar(self):
        self.driver.quit()

def main():
    extractor = EleccionesEcuadorManual()
    try:
        extractor.iniciar_extraccion_manual()
    except Exception as e:
        print(f"Error en la ejecución: {str(e)}")
    finally:
        extractor.cerrar()

if __name__ == "__main__":
    main()