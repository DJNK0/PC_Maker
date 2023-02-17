from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import scrape_data
import filter_data
# Initialiseer Selenium
driver = webdriver.Chrome()
driver.get("https://www.pythonanywhere.com/user/djnk/files/home/djnk/mysite/data/results_data")

time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="id_auth-username"]').send_keys("djnk")
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="id_auth-password"]').send_keys("_yz7s5#Vg&tXu#q")
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="id_next"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="id_upload_button"]').click()
time.sleep(1)


def upload(f_naam):
    upload_knop = driver.find_element(By.XPATH, '//*[@id="id_upload_filename"]')
    upload_knop.send_keys(f_naam)
    time.sleep(1)


upload("C:/Users/david/PycharmProjects/info/data/results_data/results_psus.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_coolers.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_moederborden.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_behuizing.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_cpus.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_gpus.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_opslag.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_ram_ddr4.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_ram_ddr5.txt")
upload("C:/Users/david/PycharmProjects/info/data/results_data/results_behuizing.txt")
