from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pandas as pd

def get_jumbo_products():
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--enable-unsafe-swiftshader")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--log-level=3")
        options.add_argument("--remote-debugging-port=0")

        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

        products = []

        #Lista de URLs y sus categorías
        base_urls = [
            ("https://www.jumbo.cl/vinos-cervezas-y-licores?page={}", "Cervezas y Licores"),
            ("https://www.jumbo.cl/lacteos-y-quesos?page={}", "Lácteos"),
            ("https://www.jumbo.cl/despensa?page={}", "Despensa"),
            ("https://www.jumbo.cl/frutas-y-verduras/verduras", "Frutas y Verduras"),
            ("https://www.jumbo.cl/frutas-y-verduras/frutas", "Frutas y Verduras"),
            ("https://www.jumbo.cl/limpieza?page={}", "Limpieza"),
            
        ]

        max_pages = 20  # Límite de páginas por categoría
        wait = WebDriverWait(driver, 10)

        # Recorremos cada URL y su categoría
        for base_url, categoria in base_urls:
            page = 1
            while page <= max_pages:
                try:
                    driver.get(base_url.format(page))
                    
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shelf-content")))
                    
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)

                    elements = driver.find_elements(By.XPATH, "//div[@data-cnstrc-item-name]")
                    if not elements:
                        break

                    for el in elements:
                        driver.execute_script("arguments[0].scrollIntoView();", el)
                        time.sleep(0.2) 

                        try:
                            name = el.get_attribute("data-cnstrc-item-name")
                        except:
                            name = "No disponible"

                        try:
                            brand = el.find_element(By.TAG_NAME, "p").text.strip()
                        except:
                            brand = "No disponible"

                        try:
                            price = el.get_attribute("data-cnstrc-item-price")
                        except:
                            price = "No disponible"

                        try:
                            image_url = el.find_element(By.TAG_NAME, "img").get_attribute("src")
                        except:
                            image_url = ""

                        try:
                            link = el.find_element(By.TAG_NAME, "a").get_attribute("href")
                        except:
                            link = ""

                        products.append({
                            "product_name": name,
                            "brand": brand,
                            "price": price,
                            "category": categoria,   
                            "market_name": "Jumbo",
                            "image_url": image_url,
                            "link": link,
                            "query_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    print(f"Productos extraídos de la página {page} de {categoria}: {len(elements)}")
                    page += 1

                except Exception as page_error:
                    print(f"Error en página {page} de categoría {categoria}: {str(page_error)}")
                    break
            print(f"{categoria} de Jumbo extraída con éxito total:{len(products)} ")


        driver.quit()
        return products

    except Exception as e:
        print(f"Error general en get_jumbo_products: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return []


if __name__ == "__main__":
    productos = get_jumbo_products()
    print(f"Total de productos obtenidos: {len(productos)}")

    productos_df = pd.DataFrame(productos)
    filename = "test.xlsx"
    productos_df.to_excel(filename, index=False)
    print(f"✅ Archivo Excel guardado como: {filename}")