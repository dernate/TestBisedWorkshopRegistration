#!/usr/bin/env python3

from . import get_catalog_text
from input import load_data
import PySimpleGUI as sg
from os.path import isfile

# The structure of the "Select XLSX file" page
page_structure = [
    [
        sg.Text(get_catalog_text("page_select_xlsxfile_headertext"))
    ],
    [
        sg.Text(get_catalog_text("page_select_xlsxfile_selecttext")),
        sg.In(size=(45, 1), key="-TEXTFIELDFILE-", disabled=True, use_readonly_for_disable=True,
              disabled_readonly_background_color="white"),
        sg.FileBrowse(button_text=get_catalog_text("page_select_xlsxfile_browsebutton"),
                      target="-TEXTFIELDFILE-")
    ],
    [
        sg.Text(get_catalog_text("page_select_xlsxfile_col_url")),
        sg.In(size=(25, 1), enable_events=True, key="-TEXTFIELDURL-")
    ],
    [
        sg.Button(button_text=get_catalog_text("page_select_xlsxfile_testregistration"), key="-BUTTON_TESTREG-"),
        sg.Button(button_text=get_catalog_text("page_select_xlsxfile_testregerr"), key="-BUTTON_TESTREGERR-", visible=False),
        sg.Button(button_text=get_catalog_text("page_select_xlsxfile_testcontent"), key="-BUTTON_TESTCONTENT-", visible=False)
    ]
]


def handle_events(event: str, values: dict) -> str or None:
    """
        Event handler for the page_select_xlsxfile page

        :param event: The event that was triggered
        :param values: The values of the elements in the window
        :return: The next page to be displayed. Either a string or None
    """
    if event == "-BUTTON_TESTREG-" or \
            event == "-BUTTON_TESTREGERR-" or \
            event == "-BUTTON_TESTCONTENT-":
        if values["-TEXTFIELDFILE-"] == "":
            sg.popup(get_catalog_text("page_select_xlsxfile_popup_nofile"))
            return None
        if values["-TEXTFIELDURL-"] == "":
            sg.popup(get_catalog_text("page_select_xlsxfile_popup_nourl"))
            return None
        if isfile(values["-TEXTFIELDFILE-"]):
            if values["-TEXTFIELDURL-"] not in load_data.xlsx_get_columns(values["-TEXTFIELDFILE-"]):
                sg.popup(get_catalog_text("page_select_xlsxfile_popup_urlheaderwrong"))
                return None
            return "-page_select_xlsxfile_finished-"
    return None
