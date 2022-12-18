from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from math import ceil

def scrape_prijs_specifiek(src):
    driver.get(src)
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    prijs = soup.find("div", {"class": "euro large"}).text
    nieuw_p = prijs.strip(",-")

    return nieuw_p

def verwerk_resultaten(f_naam, producten, prijzen):
    # Stop kaart en prijs in dictionary
    prijs_gekoppelde_producten = dict(zip(producten, prijzen))

    # Maak een file
    with open(f_naam, "w") as f:
        # Schrijf gekoppeld product/prijs naar file
        for key in prijs_gekoppelde_producten:
            if prijs_gekoppelde_producten[key] != "":
                f.write(f"{key}:{prijs_gekoppelde_producten[key]}\n")


# vind hoeveelheid producten zodat we weten hoeveel pagina's er gescrapet moeten worden
def bereken_hoeveelheid():
    # Stuur de paginabron naar selenium en BeautifulSoup
    source = driver.page_source
    soup = BeautifulSoup(source, features="html.parser")

    # Zoek het stukje tekst met het aantal producten op de pagina
    hoeveelheid = soup.find("div", {"class": "paginfo"}).text

    # Formatteer de tekst correct door alfabetische karakters te verwijderen
    hoeveelheid = re.sub("[^0-9]", "", hoeveelheid[9:13])

    # Deel hoeveelheid door 25 (De hoeveelheid producten op 1 pagina)
    return ceil(int(hoeveelheid) / 25)

# -----------------Videokaarten----------------- #
# Initialiseer Selenium
driver = webdriver.Chrome()
driver.get("https://www.megekko.nl/Computer/Componenten/videokaarten")


# Klik filters voor het merk van de kaart aan met selenium
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div/main/div[1]/div[6]/div[3]/div/div[5]/div/div[1]/label').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div/main/div[1]/div[6]/div[3]/div/div[5]/div/div[2]/label').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div/main/div[1]/div[6]/div[3]/div/div[5]/div/div[5]/label').click()
time.sleep(1)

# Maak prijzen en producten lijst
prijzen = []
producten = []

# Bereken hoeveelheid pagina's
hoeveelheid = bereken_hoeveelheid()


# Deze functie scraped de prijzen en namen van alle producten op megekko
def scrape_pagina(next_page_xpath):
    # Loep
    for i in range(hoeveelheid + 1):
        # Kopieer de html van de pagina
        source = driver.page_source
        soup = BeautifulSoup(source, features="html.parser")

        # Zoek elke a tag met de class "naam"
        producten_container = soup.find_all("a", {"class": "naam"})

        # Zoek elke div tag met de class "priceBlock"
        prijs_container = soup.find_all("div", {"class": "priceBlock"})

        # Formuleer lijst met producten
        for videokaart in producten_container:
            producten.append(videokaart.text)

        # Loep over prijs containers
        for prijs in prijs_container:
            # Vind individuele prijs
            p = prijs.find("div", {"class": "euro"})

            # Als er een prijs is verwijder ",-" zodat alleen het getal overblijft
            if p is not None:
                nieuw_p = p.text.strip(",-")

                # Voeg deze prijs toe aan lijst
                prijzen.append(nieuw_p)
            # Voeg niks toe als de prijs niet gevonden wordt
            else:
                prijzen.append("")

        time.sleep(1)
        driver.find_element(By.XPATH, next_page_xpath).click()


# Call functie om pagina te scrapen
scrape_pagina('/html/body/div/main/div[1]/div[6]/div[5]/div[3]')

# Verwerk de resultaten in een file
verwerk_resultaten("scraped_gpus.txt", producten, prijzen)

# -----------------processoren----------------- #
# Stuur selenium nieuwe link voor processoren
time.sleep(1)
driver.get("https://www.megekko.nl/Computer/Componenten/Processoren")

# Reset prijzen/producten lijst
prijzen = []
producten = []

# Klik filters voor de socket aan met selenium
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div/main/div[1]/div[5]/div[3]/div/div[5]/div/div[14]').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div/main/div[1]/div[5]/div[3]/div/div[5]/div/div[3]/label').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div/main/div[1]/div[5]/div[3]/div/div[5]/div/div[5]/label').click()
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div/main/div[1]/div[5]/div[3]/div/div[5]/div/div[10]/label').click()
time.sleep(1)

# Bereken hoeveel pagina's er zijn
hoeveelheid = bereken_hoeveelheid()

# Scrape pagina en verwerk resultaten
scrape_pagina('/html/body/div/main/div[1]/div[5]/div[5]/div[3]')
verwerk_resultaten("scraped_cpus.txt", producten, prijzen)

# -----------------Moederborden----------------- #
# Stuur selenium nieuwe link voor moederborden
time.sleep(1)
driver.get("https://www.megekko.nl/Computer/Componenten/Moederborden")

# Reset prijzen/producten lijst
prijzen = []
producten = []

# Klik meer klop
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="showmoreprodList7"]').click()
time.sleep(1)

# Klik
driver.find_element(By.XPATH, "/html/body/div/main/div[1]/div[6]/div[3]/div/div[5]/div/div[1]/label").click()
time.sleep(1)

# Klik
driver.find_element(By.XPATH, "/html/body/div/main/div[1]/div[6]/div[3]/div/div[5]/div/div[2]/label").click()
time.sleep(1)

# Klik AM5
driver.find_element(By.XPATH,"/html/body/div/main/div[1]/div[6]/div[3]/div/div[5]/div/div[5]/label").click()
time.sleep(1)
# Bereken hoeveelheid pagina's
hoeveelheid = bereken_hoeveelheid()

# Scrape pagina en verwerk resultaten
scrape_pagina("/html/body/div/main/div[1]/div[6]/div[5]/div[3]")
verwerk_resultaten("scraped_moederborden.txt", producten, prijzen)

# ----------------- Coolers ----------------- #
time.sleep(1)
prijzen = []
producten = []

# Cooler Master Hyper 212 EVO V2 R2
producten.append("Cooler Master Hyper 212 EVO V2 R2")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/1994/1040396/CPU-Luchtkoeling/Cooler-Master-Hyper-212-EVO-V2-R2"))

# Arctic Freezer 34 eSports DUO
producten.append("Arctic Freezer 34 eSports DUO")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/1994/1128917/CPU-Luchtkoeling/Arctic-Freezer-34-eSports-DUO-Wit-Wit-?s_o=1"))

# Artctic Liquid Freezer II 240
producten.append("Artic Liquid Freezer II 240")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/1986/1086852/Complete-sets-CPU/Arctic-Liquid-Freezer-II-240?s_o=1"))

verwerk_resultaten("results_coolers.txt", producten, prijzen)

# ----------------- Behuizingen ----------------- #
prijzen = []
producten = []

# Goedkoopste behuizing
driver.get("https://www.megekko.nl/Computer/Componenten/Behuizingen/Midi-Tower-Behuizingen?f=f_vrrd-3_s-prijs09_pp-50_p-1_d-list_cf-")
time.sleep(1)
producten.append(driver.find_element(By.XPATH, '//*[@id="content_list_content"]/div[1]/div/div[2]/div[4]/div/div/a/div/div[1]').text)
prijzen.append(driver.find_element(By.XPATH, '//*[@id="content_list_content"]/div[1]/div/div[2]/a/h2').text)

# Zalman t7
producten.append("Zalman T7 Midi Tower Behuizing")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/2013/1106377/Midi-Tower-Behuizingen/Zalman-T7-Midi-Tower-Behuizing?s_o=1"))

# Corsair 4000D Airflow
producten.append("Corsair 4000D Airflow Tempered Glass Black Midi Tower Behuizing")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/2013/1113622/Midi-Tower-Behuizingen/Corsair-4000D-Airflow-Tempered-Glass-Black-Midi-Tower-Behuizing?s_o=1"))

producten.append("Fractal Design Torrent Gray + Light TG Midi Tower Behuizing")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/2013/375177/Midi-Tower-Behuizingen/Fractal-Design-Torrent-Gray-Light-TG-Midi-Tower-Behuizing?s_o=3"))

verwerk_resultaten("behuizing_results.txt", producten, prijzen)

# ----------------- Opslag ----------------- #
prijzen = []
producten = []

time.sleep(1)
driver.get("https://www.megekko.nl/Computer/Componenten/Hard-disks")
time.sleep(1)
hoeveelheid = bereken_hoeveelheid()
scrape_pagina('//*[@id="navigation_products"]/div[5]/div[3]')
resultaten = verwerk_resultaten("scraped_opslag.txt", producten, prijzen)