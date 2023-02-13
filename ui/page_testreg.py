#!/usr/bin/env python3

from . import get_catalog_text
from input import load_data
from web_scrape import test_reg
import PySimpleGUI as sg
import names
from selenium import webdriver


page_structure_1 = [
    [
        sg.Text(get_catalog_text("page_testreg_headertext"))
    ],
    [
        sg.Listbox(values=[], size=(45, 20), key="-LISTBOXTESTSITES-", enable_events=True)
    ]
]

page_structure_2 = [
    [
        sg.Text(get_catalog_text("page_testreg_testcount"))
    ],
    [
        sg.Text(get_catalog_text("page_testreg_teacher")),
        sg.In(size=(3, 1), enable_events=True, key="-TEXTFIELDTEACHER-"),
        sg.Text(get_catalog_text("page_testreg_students")),
        sg.In(size=(3, 1), enable_events=True, key="-TEXTFIELDSTUDENTS-"),
        sg.Text(get_catalog_text("page_testreg_teachingstudents")),
        sg.In(size=(3, 1), enable_events=True, key="-TEXTFIELDTEACHINGSTUDENTS-"),
    ],
    [
        sg.Text(get_catalog_text("page_testreg_lkplus")),
        sg.In(size=(3, 1), enable_events=True, key="-TEXTFIELDLKPLUS-"),
        sg.Text(get_catalog_text("page_testreg_other")),
        sg.In(size=(3, 1), enable_events=True, key="-TEXTFIELDOTHER-"),
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Checkbox(get_catalog_text("page_testreg_checkbox_randomnames"), key="-CHECKBOXRANDOMNAMES-",
                    default=True, enable_events=True)
    ],
    [
        sg.Text(get_catalog_text("page_testreg_name")),
        sg.In(size=(10, 1), enable_events=True, key="-TEXTFIELDNAME-"),
        sg.Text(get_catalog_text("page_testreg_institution")),
        sg.In(size=(20, 1), enable_events=True, key="-TEXTFIELDINSTITUTION-")
    ],
    [
        sg.Text(get_catalog_text("page_testreg_prename")),
        sg.In(size=(10, 1), enable_events=True, key="-TEXTFIELDPRENAME-"),
        sg.Text(get_catalog_text("page_testreg_email")),
        sg.In(size=(20, 1), enable_events=True, key="-TEXTFIELDEMAIL-")
    ],
    [
        sg.Button(button_text=get_catalog_text("page_testreg_start"), key="-BUTTONSTART-")
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
            driver, load_data.xlsx_get_urls(xlsx_fn, xlsx_url_column), int(values["-TEXTFIELDTEACHER-"]),
            int(values["-TEXTFIELDSTUDENTS-"]), int(values["-TEXTFIELDTEACHINGSTUDENTS-"]),
            int(values["-TEXTFIELDLKPLUS-"]), int(values["-TEXTFIELDOTHER-"]), values["-TEXTFIELDNAME-"],
            values["-TEXTFIELDPRENAME-"], values["-TEXTFIELDINSTITUTION-"], values["-TEXTFIELDEMAIL-"]
        ), end_key=("-THREADSTART_TESTREG-", "-THREADEND_TESTREG-"))
    if event == "-THREADSTART_TESTREG-":
        window["-BUTTONSTART-"].update(disabled=True)
    if event == "-THREADEND_TESTREG-":
        window["-BUTTONSTART-"].update(disabled=False)
    if event == "-CHECKBOXRANDOMNAMES-":
        texts = set_random_names(values["-CHECKBOXRANDOMNAMES-"])
        for obj, t in texts.items():
            window.find_element(obj).update(t)


def set_urls(window: sg.Window, urls: list):
    window.find_element("-LISTBOXTESTSITES-").update(values=urls)


def set_random_names(random_names: bool):
    if random_names:
        lastname = names.get_last_name()
        return {
            "-TEXTFIELDNAME-": lastname,
            "-TEXTFIELDPRENAME-": names.get_first_name(),
            "-TEXTFIELDINSTITUTION-": f'{lastname} Universität'
        }
    else:
        return {}


def start_test(driver: webdriver.Chrome, urls: list, teacher: int, students: int, teaching_students: int, lkplus: int,
               other: int, name: str, prename: str, institution: str, email: str):
    for url in urls:
        try:
            err = test_reg.test_site(driver, url, teacher, students, teaching_students, lkplus, other,
                                     name, prename, institution, email)
        except Exception as e:
            sg.popup(f"Fehler beim Testen der Seite: {url}")
            print(e)
            return
        if err.error:
            sg.popup(err.errortext)
            return
    sg.popup("Test erfolgreich beendet!")
