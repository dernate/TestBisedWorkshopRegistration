#!/usr/bin/env python3

import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver")

# browser = webdriver.Chrome(executable_path = DRIVER_BIN)

#op = webdriver.ChromeOptions()
#op.add_argument('headless')
DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))#, options=op)

TEST_SITES = [
    #"http://wwwhomes.uni-bielefeld.de/bised/23-demokratie.html",
    #"http://wwwhomes.uni-bielefeld.de/bised/23-bieneprogramm.html",
    #"http://wwwhomes.uni-bielefeld.de/bised/23-rassismuskritik.html",
    #"http://wwwhomes.uni-bielefeld.de/bised/23-inklusivediag.html",
    #"http://wwwhomes.uni-bielefeld.de/bised/23-eltern.html",
    #"http://wwwhomes.uni-bielefeld.de/bised/23-halt.html",
    "http://wwwhomes.uni-bielefeld.de/bised/23-wupo.html"
]

# TEST_SITES = ["http://wwwhomes.uni-bielefeld.de/bised/23-wetterkunst.html"]


def fill_form(driver, website, dropdown_value, skip=None):
    if skip is None:
        skip = []
    driver.get(website)
    if 1 in skip:
        lastname = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[1]/input")
        lastname.send_keys("mein-Nachname")
    if 2 in skip:
        firstname = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[2]/input")
        firstname.send_keys("mein Vorname")
    if 3 in skip:
        institution = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[3]/input")
        institution.send_keys("meine Institution")
    if 4 in skip:
        mail1 = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[4]/input")
        mail1.send_keys("ginny.fuchsbau@gmx.de")
    if 5 in skip:
        mail2 = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[5]/input")
        mail2.send_keys("ginny.fuchsbau@gmx.de")
    if 6 in skip:
        status = Select(driver.find_element(By.XPATH, "//*[@id=\"status\"]"))
        status.select_by_index(dropdown_value)
    if 7 in skip:
        mail1 = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[4]/input")
        mail1.send_keys("ginnyy.fuchsbau@gmx.de")
        mail2 = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[5]/input")
        mail2.send_keys("ginny.fuchsbau@gmx.de")

    button = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[6]/input")
    button.click()
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/center/h1")))
    # print(" ")
    #return
    if skip:
        errtext = driver.find_element(By.XPATH, "/html/body/center/h1")
        if errtext.text not in ["Bitte füllen Sie das Formular vollständig aus und klicken Sie erneut auf Anmelden.",
                            "Ihre Mail-Adressen stimmen nicht überein. Bitte überprüfen Sie Ihre Angaben und klicken Sie erneut auf Anmelden."]:
            print("Fehlermeldung nicht korrekt", website, dropdown_value, skip)







values_for_status_field = list(range(1, 6))

for ts in TEST_SITES:
    for v in values_for_status_field:
        fill_form(DRIVER, ts, v, [2,3,4,5,6])
        fill_form(DRIVER, ts, v, [1,3,4,5,6])
        #fill_form(DRIVER, ts, v, [1,2,4,5,6])
        fill_form(DRIVER, ts, v, [1,2,3,5,6])
        fill_form(DRIVER, ts, v, [1,2,3,4,6])
        fill_form(DRIVER, ts, v, [1,2,3,4,5])
        fill_form(DRIVER, ts, v, [1,2,3,6,7])
        continue

        #if v == 2:
        #    for _ in range(0, 2):
        #        fill_form(DRIVER, ts, v, [1, 2, 4, 5, 6])
        #continue

        if v == 1:
            for _ in range(0, 81):#Lehrkräfte
                fill_form(DRIVER, ts, v, [1, 2, 4, 5, 6])
        else:
            #fill_form(DRIVER, ts, 2, [1, 2, 4, 5, 6])
            #break
            for _ in range(0, 21):#sonstige
                fill_form(DRIVER, ts, v, [1, 2, 4, 5, 6])

        # print(v, "done")

DRIVER.quit()
