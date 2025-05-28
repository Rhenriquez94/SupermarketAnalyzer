#  SuperMarketAnalyzer: ETL de precios de supermercados para analizar su historico con Python, PostgreSQL y AWS

SuperMarketAnalyzer es un pipeline ETL desarrollado para extraer, transformar y almacenar precios de supermercados chilenos. Este proyecto está pensado para monitorear la evolución de precios por producto, supermercado y fecha, permitiendo análisis de mercado eficientes y automatizados.
![image](https://github.com/user-attachments/assets/899668a2-cfac-4a41-9ab7-738b10ef3840)


---

## 🧱 Arquitectura

```
Scraping (Selenium)
   ↓
Transformación (pandas)
   ↓
CSV Local (.csv)
   ↓
Carga a PostgreSQL (raw > dim & fact)
   ↓
Exportación opcional a AWS S3
```

---

## 🗂️ Estructura del proyecto

```
BeerAnalyzer/
│
├── data/
│   └── productos_totales/         ← CSVs generados por scraping
│
├── pipeline/
│   ├── load.py                    ← Carga a PostgreSQL
│   ├── save_s3.py                 ← Exporta CSV a AWS S3
│   ├── transform.py               ← Limpieza y normalización
│
├── scrapper/
│   ├── jumbo.py                   ← Scraping Jumbo
│   ├── lider.py                   ← Scraping Lider
│   ├── santa_isabel.py           ← Scraping Santa Isabel
│   └── tottus.py                  ← Scraping Tottus
│
├── sql_scripts/
│   ├── step1_update_raw.sql       ← Normalización raw
│   ├── step2_create_dim_products.sql
│   └── step3_create_fact_prices.sql
│
├── connect.py                     ← Conexión a PostgreSQL
├── main.py                        ← Script principal (orquestación)
├── .env                           ← Variables de entorno
└── README.md
```

---

## 🧪 Funcionalidades principales

- ✅ Scraping automatizado de 4 supermercados
- ✅ Transformación de datos sucios a estructurados
- ✅ Identificación de productos únicos con ID persistente
- ✅ Carga a base de datos PostgreSQL en esquema tipo DW:
  - `raw_products`
  - `dim_products`
  - `fact_prices`
- ✅ Exportación a AWS S3 para respaldo externo

---

## 🧠 Base de Datos

### raw_products

| Columna       | Tipo      |
|---------------|-----------|
| product_name  | TEXT      |
| brand         | TEXT      |
| price         | NUMERIC   |
| category      | TEXT      |
| market_name   | TEXT      |
| image_url     | TEXT      |
| link          | TEXT      |
| query_date    | TIMESTAMP |

---

## ☁️ Infraestructura y Seguridad (AWS)

Este proyecto se ejecuta en una instancia EC2 de AWS con las siguientes configuraciones:

- 🔐 **Autenticación segura con IAM Roles** para:
  - Acceso controlado a bucket S3
  - Restricción de permisos mínimos (principio de menor privilegio)
- ☁️ **Bucket S3 privado** con políticas para almacenamiento de `.csv`
- 🔒 **Ambiente virtual y variables protegidas (.env)**

---

## 🚀 Ejecución

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar scraping + carga + modelado
python main.py
```

---

## 📦 Requerimientos

- Python 3.12+
- PostgreSQL 13+
- Librerías:
  - selenium
  - pandas
  - sqlalchemy
  - psycopg2
  - webdriver-manager
  - python-dotenv
  - boto3 (opcional para S3)

Instalar:

```bash
pip install -r requirements.txt
```

---

## 📊 ¿Qué puedes hacer con este proyecto?

- Ver evolución de precios por marca, fecha y supermercado
- Comparar promociones entre supermercados
- Detectar cambios bruscos en precios
- Usarlo como base para dashboard en Power BI / Tableau

---

## 🧩 Próximos pasos (opcional)

- [ ] Orquestación con Apache Airflow o AWS Step Functions
- [ ] Frontend con React para visualización
- [ ] Alerts automáticos si suben precios

---

## 👨‍💻 Autor

Desarrollado por [Rodrigo Henríquez](https://github.com/Rhenriquez94).

---
