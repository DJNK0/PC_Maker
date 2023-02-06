import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas
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
driver.find_element(By.XPATH, '//*[@id="labelzoek_20-2"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="labelzoek_20-3"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="labelzoek_20-23"]').click()
time.sleep(1)

# Maak prijzen en producten lijst
prijzen = []
producten = []

# Bereken hoeveelheid pagina's
hoeveelheid = bereken_hoeveelheid()

# Deze functie scraped de prijzen en namen van alle producten op megekko
def scrape_pagina(next_page_xpath, naam_toevoeging =""):
    # Loep
    for i in range(hoeveelheid + 1):
        # Kopieer de html van de pagina
        source = driver.page_source
        soup = BeautifulSoup(source, features="html.parser")

        # Zoek elke a tag met de class "naam"
        producten_container = soup.find_all("a", {"class": "naam"})

        # Als ie leeg is
        if producten_container == []:
            producten_container = soup.find_all("h2", {"itemprop": "name"})

        # Zoek elke div tag met de class "priceBlock"
        prijs_container = soup.find_all("div", {"class": "priceBlock"})

        # Formuleer lijst met producten
        for videokaart in producten_container:
            # Maak alles kleine letters en verwijder extra lege lijnen
            producten.append(videokaart.text.replace("\n", "").lower() + naam_toevoeging)

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
scrape_pagina('//*[@id="navigation_products"]/div[5]/div[3]')

# Verwerk de resultaten in een file
verwerk_resultaten("scraped_gpus.txt", producten, prijzen)

# ----------------- Voedingen ----------------- # corsair nog toevoegen!!!
producten = []
prijzen = []
hoeveelheid = 1

driver.get("https://www.megekko.nl/Computer/Componenten/Voedingen/PC-voedingen/PC-Voedingen-PSU-?f=f_569-86100_vrrd-0_merk-207,24,151,259,61,135,255,104_s-populair_pp-250_p-1_d-list_cf-")
scrape_pagina('//*[@id="list_bottomheader"]/div/div[2]/div[3]/img', naam_toevoeging=" bronze")

driver.get("https://www.megekko.nl/Computer/Componenten/Voedingen/PC-voedingen/PC-Voedingen-PSU-?f=f_569-86092_vrrd-0_merk-207,24,151,259,61,135,255,104_s-populair_pp-250_p-1_d-list_cf-")
scrape_pagina('//*[@id="list_bottomheader"]/div/div[2]/div[3]/img', naam_toevoeging=" gold")

driver.get("https://www.megekko.nl/Computer/Componenten/Voedingen/PC-voedingen/PC-Voedingen-PSU-?f=f_569-86093_vrrd-0_merk-207,24,151,259,61,135,255,104_s-populair_pp-250_p-1_d-list_cf-")
scrape_pagina('//*[@id="list_bottomheader"]/div/div[2]/div[3]/img', naam_toevoeging=" platinum")

driver.get("https://www.megekko.nl/Computer/Componenten/Voedingen/PC-voedingen/PC-Voedingen-PSU-?f=f_569-86096_vrrd-0_merk-207,24,151,259,61,135,255,104_s-populair_pp-250_p-1_d-list_cf-")
scrape_pagina('//*[@id="list_bottomheader"]/div/div[2]/div[3]/img', naam_toevoeging=" titanium")
verwerk_resultaten("scraped_psus.txt", producten, prijzen)

# -----------------processoren----------------- #
# Stuur selenium nieuwe link voor processoren
time.sleep(1)
driver.get("https://www.megekko.nl/Computer/Componenten/Processoren")

# Reset prijzen/producten lijst
prijzen = []
producten = []

# Klik filters voor de socket aan met selenium
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="labelzoek_18-33"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="labelzoek_18-19"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="showmoreprodList18"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="labelzoek_18-34"]').click()
time.sleep(1)

# Bereken hoeveel pagina's er zijn
hoeveelheid = bereken_hoeveelheid()

# Scrape pagina en verwerk resultaten
scrape_pagina('//*[@id="navigation_products"]/div[5]/div[3]/img')
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
driver.find_element(By.XPATH, '//*[@id="labelzoek_7-29"]').click()
time.sleep(1)

driver.find_element(By.XPATH, '//*[@id="labelzoek_7-19"]').click()
time.sleep(1)

# Klik
driver.find_element(By.XPATH, '//*[@id="labelzoek_7-30"]').click()
time.sleep(1)

# Klik AM5
driver.find_element(By.XPATH,'//*[@id="navigation_filter"]').click()
time.sleep(1)
# Bereken hoeveelheid pagina's
hoeveelheid = bereken_hoeveelheid()

# Scrape pagina en verwerk resultaten
scrape_pagina('//*[@id="navigation_products"]/div[5]/div[3]')
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
producten.append("Aerocool Hexform")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/2012/1073924/Micro-ATX-Behuizingen/Aerocool-Hexform-Mini-Tower-Zwart-Micro-ATX-Behuizing"))

# Corsair 4000D Airflow
producten.append("Corsair 4000D Airflow Tempered Glass Black Midi Tower Behuizing")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/2013/1113622/Midi-Tower-Behuizingen/Corsair-4000D-Airflow-Tempered-Glass-Black-Midi-Tower-Behuizing?s_o=1"))

producten.append("Fractal Design Torrent Gray + Light TG Midi Tower Behuizing")
prijzen.append(scrape_prijs_specifiek("https://www.megekko.nl/product/2013/1130111/Midi-Tower-Behuizingen/Corsair-5000D-Airflow-Tempered-Glass-Black-Midi-Tower-Behuizing?s_o=2"))

verwerk_resultaten("behuizing_results.txt", producten, prijzen)

# ----------------- Opslag ----------------- #
prijzen = []
producten = []

time.sleep(1)
driver.get("https://www.megekko.nl/Computer/Componenten/Hard-disks")
time.sleep(1)
hoeveelheid = bereken_hoeveelheid()
scrape_pagina('//*[@id="navigation_products"]/div[5]/div[3]')
verwerk_resultaten("scraped_opslag.txt", producten, prijzen)

# ----------------- DDR4 Ram ----------------- #
prijzen = []
producten = []

time.sleep(1)
driver.get("https://www.megekko.nl/Computer/Componenten/Geheugen")
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="labelzoek_8-8"]').click()
time.sleep(1)
hoeveelheid = bereken_hoeveelheid()
scrape_pagina('//*[@id="navigation_products"]/div[5]/div[3]')
verwerk_resultaten("scraped_ram_ddr4.txt", producten, prijzen)

# ----------------- DDR5 Ram ----------------- #
prijzen = []
producten = []

time.sleep(1)
driver.quit()
driver = webdriver.Chrome()
driver.get("https://www.megekko.nl/Computer/Componenten/Geheugen")
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="checkProductList8-18"]').click()
time.sleep(1)
hoeveelheid = bereken_hoeveelheid()
scrape_pagina('//*[@id="navigation_products"]/div[5]/div[3]')
verwerk_resultaten("scraped_ram_ddr5.txt", producten, prijzen)

