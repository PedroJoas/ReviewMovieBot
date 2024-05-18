import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.chrome.options import Options
import pandas as pd


def retonar_elenco(nome_elenco):
        options = Options()
        options.add_argument("--headless")
        driver = None
        try:
            driver = webdriver.Chrome(options=options)

            # Exemplo de url do filme: https://www.rottentomatoes.com/m/kingdom_of_the_planet_of_the_apes/reviews
            # Os espaços nos nomes do filmes são preenchidos por _

            nome_elenco = '_'.join(re.findall(r'\b[A-zÀ-úü]+\b', nome_elenco.lower()))
            

            url = f"https://www.rottentomatoes.com/celebrity/{nome_elenco}"

            driver.get(url)
            buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "celebrity-filmography__audience-score-header"))
            )
            
            button_audience_score = buttons[0]
            
            button_audience_score.click()
            
            tbody = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-qa="celebrity-filmography-movies"]'))
            )

            table_html = tbody.get_attribute("innerHTML")
            
            df = pd.read_html(table_html)

            
            #print(df.head())

        finally:
            if driver:
                driver.quit()


retonar_elenco("george lucas")

