#!/usr/bin/env python3

from . import get_catalog_text
from input import load_data
from web_scrape import test_err
import PySimpleGUI as sg
import names
from selenium import webdriver


page_structure_1 = [
    [
        sg.Text(get_catalog_text("page_testerr_headertext"))
    ],
    [
        sg.Listbox(values=[], size=(45, 20), key="-LISTBOXTESTSITES-", enable_events=True)
    ]
]

page_structure_2 = [
    [
        sg.Text(get_catalog_text("page_testerr_preferences"))
    ],
    [
        sg.Checkbox(get_catalog_text("page_testerr_checkbox_missing"), key="-CHECKBOXMISSING-",
                    default=True, enable_events=True)
    ],
    [
        sg.Checkbox(get_catalog_text("page_testerr_checkbox_maildifferent"), key="-CHECKBOXMAILDIFFERENT-",
                    default=True, enable_events=True)
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Checkbox(get_catalog_text("page_testerr_checkbox_randomnames"), key="-CHECKBOXRANDOMNAMESERR-",
                    default=True, enable_events=True)
    ],
    [
        sg.Text(get_catalog_text("page_testerr_name")),
        sg.In(size=(10, 1), enable_events=True, key="-TEXTFIELDERRNAME-"),
        sg.Text(get_catalog_text("page_testerr_prename")),
        sg.In(size=(10, 1), enable_events=True, key="-TEXTFIELDERRPRENAME-")
    ],
    [
        sg.Text(get_catalog_text("page_testerr_institution")),
        sg.In(size=(20, 1), enable_events=True, key="-TEXTFIELDERRINSTITUTION-")
    ],
    [
        sg.Text(get_catalog_text("page_testerr_email")),
        sg.In(size=(20, 1), enable_events=True, key="-TEXTFIELDERREMAIL-"),
        sg.Text(get_catalog_text("page_testerr_email2")),
        sg.In(size=(20, 1), enable_events=True, key="-TEXTFIELDERREMAIL2-")
    ],
    [
        sg.Button(button_text=get_catalog_text("page_testerr_start"), key="-BUTTONSTARTERR-")
    ]
]

page_structure = [
    [
        sg.Column(page_structure_1),
        sg.VSeparator(),
        sg.Column(page_structure_2)
    ]
]


def set_preset_values(window: sg.Window, presetvalues: dict, random_names: bool):
    for obj, pv in presetvalues.items():
        window.find_element(obj).update(pv)
    texts = set_random_names(random_names)
    for obj, t in texts.items():
        window.find_element(obj).update(t)


def handle_events(event: str, values: dict, window: sg.Window, driver: webdriver.Chrome, xlsx_fn, xlsx_url_column):
    if event == "-BUTTONSTART-":
        window.start_thread(func=lambda: start_test(
            driver, load_data.xlsx_get_urls(xlsx_fn, xlsx_url_column),
            bool(values["-CHECKBOXMISSING-"]), bool(values["-CHECKBOXMAILDIFFERENT-"]),
            values["-TEXTFIELDERRNAME-"], values["-TEXTFIELDERRPRENAME-"],
            values["-TEXTFIELDERRINSTITUTION-"], values["-TEXTFIELDERREMAIL-"], values["-TEXTFIELDERREMAIL2-"]
        ), end_key=("-THREADSTART_TESTREG-", "-THREADEND_TESTREG-"))
    if event == "-THREADSTART_TESTREG-":
        window["-BUTTONSTART-"].update(disabled=True)
    if event == "-THREADEND_TESTREG-":
        window["-BUTTONSTART-"].update(disabled=False)
    if event == "-CHECKBOXRANDOMNAMESERR-":
        texts = set_random_names(values["-CHECKBOXRANDOMNAMESERR-"])
        for obj, t in texts.items():
            window.find_element(obj).update(t)


def set_urls(window: sg.Window, urls: list):
    window.find_element("-LISTBOXTESTSITES-").update(values=urls)


def set_random_names(random_names: bool):
    if random_names:
        lastname = names.get_last_name()
        return {
            "-TEXTFIELDERRNAME-": lastname,
            "-TEXTFIELDERRPRENAME-": names.get_first_name(),
            "-TEXTFIELDERRINSTITUTION-": f'{lastname} Universität'
        }
    else:
        return {}


def get_testcases_missing(name: str, prename: str, institution: str, email: str):
    return [
        {
            "name": "",
            "prename": prename,
            "institution": institution,
            "email": email,
            "email2": email
        },
        {
            "name": name,
            "prename": "",
            "institution": institution,
            "email": email,
            "email2": email
        },
        {
            "name": name,
            "prename": prename,
            "institution": institution,
            "email": "",
            "email2": ""
        }
    ]


def start_test(driver: webdriver.Chrome, urls: list, test_missing: bool, test_mail_different: bool,
               name: str, prename: str, institution: str, email: str, email2: str):
    result = []
    if test_missing:
        # Test missing inputs
        testcases = get_testcases_missing(name, prename, institution, email)
        for url in urls:
            try:
                err = test_err.test_site(driver, url, testcases, "/html/body/center/h1")
            except Exception as e:
                sg.popup(f"Fehler beim Testen der Seite: {url}")
                print(e)
                return
            if err.error:
                sg.popup(err.errortext)
                return
        result.append("Test mit fehlenden Eingaben erfolgreich beendet!")
    if test_mail_different:
        # Test different emails
        if email == email2:
            sg.popup("Die E-Mail-Adressen sind gleich, bitte verschiedene eintragen zum testen!")
            return
        for url in urls:
            try:
                err = test_err.test_site(driver, url, [{
                    "name": name,
                    "prename": prename,
                    "institution": institution,
                    "email": email,
                    "email2": email2
                }], "/html/body/center/h1")
            except Exception as e:
                sg.popup(f"Fehler beim Testen der Seite: {url}")
                print(e)
                return
            if err.error:
                sg.popup(err.errortext)
                return
        result.append("Test mit unterschiedlichen E-Mail-Adressen erfolgreich beendet!")
    for r in result:
        sg.popup(r)
