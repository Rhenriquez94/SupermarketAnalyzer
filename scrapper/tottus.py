def get_tottus_products():
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

        products = []

        base_urls = [
            ("https://www.tottus.cl/tottus-cl/lista/CATG27059/Conservas-y-Enlatados", "Despensa"),
            # ... (las demás categorías que ya tienes)
        ]

        max_pages = 5
        wait = WebDriverWait(driver, 10)
        MAX_RETRIES = 3
        RETRY_DELAY = 3

        for base_url, categoria in base_urls:
            page = 1
            driver.get(base_url)

            while page <= max_pages:
                retries = 0
                success = False

                while retries < MAX_RETRIES and not success:
                    try:
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.pod-link')))
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)

                        elements = driver.find_elements(By.CSS_SELECTOR, 'a.pod-link')
                        if not elements:
                            print(f"No se encontraron productos en página {page} de {categoria}")
                            break

                        for el in elements:
                            driver.execute_script("arguments[0].scrollIntoView();", el)
                            time.sleep(0.5)

                            try:
                                name = el.find_element(By.CSS_SELECTOR, 'b.pod-subTitle').text.strip()
                            except:
                                name = "No disponible"

                            try:
                                brand = el.find_element(By.CSS_SELECTOR, 'b.title-rebrand').text.strip()
                            except:
                                brand = "No disponible"

                            try:
                                price = el.find_element(By.TAG_NAME, 'li').get_attribute('data-internet-price')
                            except:
                                price = "No disponible"

                            try:
                                image_url = el.find_element(By.CSS_SELECTOR, 'source').get_attribute('srcset')
                            except NoSuchElementException:
                                try:
                                    image_url = el.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                                except NoSuchElementException:
                                    image_url = ""

                            try:
                                link = el.get_attribute("href")
                            except:
                                link = ""

                            products.append({
                                "product_name": name,
                                "brand": brand,
                                "price": price,
                                "category": categoria,
                                "market_name": "Tottus",
                                "image_url": image_url,
                                "link": link,
                                "query_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })

                        success = True
                        page += 1
                        print(f"Productos extraídos de la página {page} de {categoria}: {len(elements)}")

                        try:
                            next_button = wait.until(EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, "button#testId-pagination-bottom-arrow-right")
                            ))
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", next_button)
                        except TimeoutException:
                            print(f"🔚 Fin de la paginación en página {page} (botón siguiente no disponible).")
                            break
                        except Exception as e:
                            print(f"❌ No se pudo hacer clic en siguiente en página {page}: {e}")
                            break

                    except TimeoutException:
                        retries += 1
                        print(f"Timeout en página {page}. Reintentando ({retries}/{MAX_RETRIES})...")
                        time.sleep(RETRY_DELAY)

                    except Exception as page_error:
                        print(f"Error inesperado en página {page}: {str(page_error)}")
                        retries = MAX_RETRIES
                        break

                if not success:
                    print(f"No se pudo procesar la página {page} después de {MAX_RETRIES} intentos.")
                    break

            print(f"Cerveza de Tottus extraída con éxito total: {len(products)}")

        driver.quit()
        return products

    except Exception as e:
        print(f"❌ Error general en get_tottus_products: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return []
