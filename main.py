#!/usr/bin/env python3

from ui import page_select_xlsxfile, page_testreg, page_testerr
from input import load_data
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import PySimpleGUI as sg

DRIVER = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

current_window = None
WINDOW1 = "Datenbasis auswählen"
WINDOW2 = "Teste Anmeldungen"
WINDOW3 = "Teste Fehler"
WINDOW4 = "Teste Inhalt"

WINDOWS = {
    "-BUTTON_TESTREG-": WINDOW2,
    "-BUTTON_TESTREGERR-": WINDOW3,
    "-BUTTON_TESTCONTENT-": WINDOW4
}


def set_window(button_clicked: str) -> str:
    """
    Returns the window to be displayed next in dependence of the button that was clicked. Default is WINDOW1.
    Set initial parameters for the next window.
    :param button_clicked: event string from clicked button
    :return: window name
    """
    return WINDOWS.get(button_clicked, WINDOW1)


if __name__ == "__main__":
    current_window = WINDOW1
    window = sg.Window(current_window, page_select_xlsxfile.page_structure).finalize()
    window.find_element("-TEXTFIELDURL-").update("url")
    xlsx_fn, xlsx_url_column = "", ""

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if current_window == WINDOW1:
            changes = page_select_xlsxfile.handle_events(event, values)
        elif current_window == WINDOW2:
            page_testreg.handle_events(event, values, window, DRIVER, xlsx_fn, xlsx_url_column)
            changes = None
        elif current_window == WINDOW3:
            page_testerr.handle_events(event, values, window, DRIVER, xlsx_fn, xlsx_url_column)
            changes = None
        else:
            changes = None
        if changes is not None:
            if changes == "-page_select_xlsxfile_finished-":
                current_window = set_window(event)
                if current_window == WINDOW1:
                    continue
                xlsx_fn = values["-TEXTFIELDFILE-"]
                xlsx_url_column = values["-TEXTFIELDURL-"]
                window.close()
                if current_window == WINDOW2:
                    window = sg.Window(current_window, page_testreg.page_structure, finalize=True)
                    presetvalues = {
                        "-TEXTFIELDTEACHER-": 10,
                        "-TEXTFIELDSTUDENTS-": 10,
                        "-TEXTFIELDTEACHINGSTUDENTS-": 10,
                        "-TEXTFIELDLKPLUS-": 10,
                        "-TEXTFIELDOTHER-": 10
                        # weitere ausfüllen und aus datei lesen und abspeichern
                    }
                    page_testreg.set_preset_values(window=window, presetvalues=presetvalues, random_names=True)
                    page_testreg.set_urls(window=window, urls=load_data.xlsx_get_urls(xlsx_fn, xlsx_url_column))
                elif current_window == WINDOW3:
                    window = sg.Window(current_window, page_testerr.page_structure, finalize=True)
                    page_testerr.set_preset_values(window=window, presetvalues={}, random_names=True)
                    page_testerr.set_urls(window=window, urls=load_data.xlsx_get_urls(xlsx_fn, xlsx_url_column))

    window.close()
    DRIVER.quit()
