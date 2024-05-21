import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

def retonar_sinopse(nome_filme):
        options = Options()
        options.add_argument("--headless")
        driver = None
        try:
            driver = webdriver.Chrome(options=options)

            # Exemplo de url do filme: https://www.rottentomatoes.com/m/kingdom_of_the_planet_of_the_apes/reviews
            # Os espaços nos nomes do filmes são preenchidos por _

            nome_filme = '_'.join(re.findall(r'\b[A-zÀ-úü]+\b', nome_filme.lower()))
            

            url = f"https://www.rottentomatoes.com/m/{nome_filme}"

            driver.get(url)
            
            sinopse = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//drawer-more[@slot="description"]'))
            )

            return sinopse.text


        finally:
            if driver:
                driver.quit()


print(retonar_sinopse("me before you"))

