#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, WebDriverException
from test_reg import click_btn
from ui.errors import ErrWebTest


def fill_form(driver: webdriver.Chrome, name: str or None, prename: str or None, institution: str or None,
              email1: str or None, email2: str or None, dropdown_value: int or None):
    if name:
        lastname = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[1]/input")
        lastname.send_keys(name)
    if prename:
        firstname = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[2]/input")
        firstname.send_keys(prename)

    if institution:
        ins = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[3]/input")
        ins.send_keys(institution)

    if email1:
        mail1 = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[4]/input")
        mail1.send_keys(email1)

    if email2:
        mail2 = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[5]/input")
        mail2.send_keys(email2)

    if dropdown_value:
        status = Select(driver.find_element(By.XPATH, "//*[@id=\"status\"]"))
        status.select_by_index(dropdown_value)


def test_site(driver: webdriver.Chrome, url: str, testcases: list, expected_result_xpath: str) -> ErrWebTest:
    for testcase in testcases:
        try:
            driver.get(url)
        except WebDriverException:
            return ErrWebTest(True, f"Fehler beim Aufruf der Seite: {url}")
        fill_form(
            driver,
            testcase.get("name", None),
            testcase.get("prename", None),
            testcase.get("institution", None),
            testcase.get("email", None),
            testcase.get("email2", None),
            testcase.get("ddv", None)
        )
        err = click_btn(
            driver,
            "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[6]/input",
            15,
            expected_result_xpath
        )
        if err.error:
            return err
        errtext = driver.find_element(By.XPATH, "/html/body/center/h1")
        if errtext.text not in ["Bitte füllen Sie das Formular vollständig aus und klicken Sie erneut auf Anmelden.",
                                "Ihre Mail-Adressen stimmen nicht überein. Bitte überprüfen Sie Ihre Angaben und "
                                "klicken Sie erneut auf Anmelden."]:
            return ErrWebTest(True, f"Unerwarteter Text: {errtext.text}")
    return ErrWebTest(False)
