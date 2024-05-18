import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

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
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="celebrity-filmography-movies"]'))
            )

            table_html = tbody.get_attribute("innerHTML")

            soup = BeautifulSoup(table_html, "html.parser")
            # Extract table rows
            table_rows = soup.find_all('tr')

            # Create empty list to store table data
            table_data = []

            # Iterate through rows and extract data from each cell
            for row in table_rows:
                row_data = []
                for cell in row.find_all('td'):
                    row_data.append(cell.text.strip("\n"))    
                table_data.append(row_data)

            titulos_top10 = []
            for row in table_data[1:11]:
                titulos_top10.append(row[2])

            return titulos_top10


        finally:
            if driver:
                driver.quit()


retonar_elenco("george lucas")

