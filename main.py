from scrapper.jumbo import get_jumbo_products
from scrapper.lider import get_lider_products
from scrapper.santa_isabel import get_sta_isabel_products
from scrapper.tottus import get_tottus_products
from pipeline.transform import clean_data
from pipeline.load import save_to_csv
from sql_scripts.sql_load import cargar_csvs_en_raw
from connect import connect  
import time
from sqlalchemy import text
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Función para ejecutar scripts SQL
def ejecutar_sql_script(path_sql_file, engine):
    with open(path_sql_file, 'r', encoding='utf-8') as file:
        sql_script = file.read()
    with engine.connect() as connection:
        connection.execute(text(sql_script))
        connection.commit()

# Configuración de tiempo de espera
start_time = time.time()

if __name__ == "__main__":
    print("Iniciando scraping de Jumbo...")
    productos_jumbo = get_jumbo_products()

    print("Iniciando scraping de Lider...")
    productos_lider = get_lider_products()

    print("Iniciando scraping de Santa Isabel...")
    productos_staisabel = get_sta_isabel_products()

    print("Iniciando scraping de Tottus...")
    productos_tottus = get_tottus_products()

    # Unificar productos
    productos_fin = productos_jumbo + productos_lider + productos_staisabel + productos_tottus

    if productos_fin:
        df = clean_data(productos_fin)
        save_to_csv(df, "productos_totales")
        print(f"✅ Archivo creado! Total de productos obtenidos: {len(df)}")

        end_time = time.time()
        elapsed_seconds = int(end_time - start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        print(f"⏱ Tiempo de ejecución del scraping: {minutes:02d}:{seconds:02d} minutos")

        # Paso 1: Cargar CSV a RAW (cargar en la tabla de base de datos)
        print("📥 Cargando archivos CSV a RAW...")
        cargar_csvs_en_raw()

        # Paso 2: Ejecutar scripts de modelado en base de datos
        print("⚙️ Ejecutando scripts SQL de modelado...")
        engine = connect()

        scripts_etl = [
            os.path.join(BASE_DIR,"sql_scripts/step1_update_raw.sql"),
            os.path.join(BASE_DIR,"sql_scripts/step2_create_dim_products.sql"),
            os.path.join(BASE_DIR,"sql_scripts/step3_create_fact_prices.sql"),  
        ]

        for script_path in scripts_etl:
            try:
                ejecutar_sql_script(script_path, engine)
                print(f"✅ Terminado: {script_path}")
            except Exception as e:
                print(f"❌ Error ejecutando {script_path}: {e}")
                break

        print("🎯 ETL completo: scraping + carga + modelado.")
    else:
        print("⚠️ No se encontraron productos. No se ejecutó carga ni modelado.")

save_to_csv(df, "productos_totales", bucket_name="beer-analyzer-data")


