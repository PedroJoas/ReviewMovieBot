from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def reviews(filme):
    driver = webdriver.Chrome()
    # Exemplo de url do filme: https://www.rottentomatoes.com/m/kingdom_of_the_planet_of_the_apes/reviews
    # Os espaços nos nomes do filmes são preenchidos por _

    filme = filme.lower().replace(" ", "_")

    url = f"https://www.rottentomatoes.com/m/{filme}/reviews"

    driver.get(url)

    cont = 0
    while(cont < 3):
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "rt-button"))
        )

        button.click()
        cont += 1

        sleep(1)

    sleep(1)

    texts = [t.text for t in driver.find_elements(By.CLASS_NAME, "review-text")]

    driver.quit()

    return texts

