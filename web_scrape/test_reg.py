#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from ui.errors import ErrWebTest
from random import shuffle


def fill_form(driver: webdriver.Chrome, name: str, prename: str, institution: str, email: str, dropdown_value: int):
    lastname = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[1]/input")
    lastname.send_keys(name)

    firstname = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[2]/input")
    firstname.send_keys(prename)

    ins = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[3]/input")
    ins.send_keys(institution)

    mail1 = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[4]/input")
    mail1.send_keys(email)

    mail2 = driver.find_element(By.XPATH, "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[5]/input")
    mail2.send_keys(email)

    status = Select(driver.find_element(By.XPATH, "//*[@id=\"status\"]"))
    status.select_by_index(dropdown_value)


def click_btn(driver: webdriver.Chrome, btn_xpath: str, timeout: int, waitfor_xpath: str) -> ErrWebTest:
    button = driver.find_element(By.XPATH, btn_xpath)
    button.click()
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, waitfor_xpath)))
    except TimeoutException as ex:
        return ErrWebTest(True, "TimeoutException: " + str(ex))
    return ErrWebTest(False)


def dropdown_values_to_list(teacher: int, students: int, teaching_students: int, lkplus: int, other: int) -> list:
    values_teacher = []
    values_teacher.extend([1] * teacher)
    values_other = []
    values_other.extend([2] * students)
    values_other.extend([3] * teaching_students)
    values_other.extend([4] * lkplus)
    values_other.extend([5] * other)
    shuffle(values_other)
    return values_teacher + values_other


def test_site(driver: webdriver.Chrome, url: str, teacher: int, students: int, teaching_students: int, lkplus: int,
              other: int, name: str, prename: str, institution: str, email: str) -> ErrWebTest:
    # ToDo: get the dropdown value from the url via hidden browser
    dropdown_values = dropdown_values_to_list(teacher, students, teaching_students, lkplus, other)
    for ddv in dropdown_values:
        retry = 0
        while retry < 3:
            try:
                driver.get(url)
                break
            except WebDriverException:
                retry += 1
        if retry >= 3:
            return ErrWebTest(True, f"Fehler beim Aufruf der Seite: {url}")
        fill_form(driver, name, prename, institution, email, ddv)
        err = click_btn(
            driver,
            "//*[@id=\"main\"]/div[1]/center/table/tbody/tr/td/form/p[6]/input",
            15,
            "/html/body/center/h1"
        )
        if err.error:
            return err
    return ErrWebTest(False)
