#!/usr/bin/env python3

LANGUAGE_GERMAN = "german"

LANGUAGE_USING = LANGUAGE_GERMAN

CATALOG = {
    "page_select_xlsxfile_headertext": {
        LANGUAGE_GERMAN: "Es werden Informationen zu den zu testenden Webseiten aus einer Excel Tabelle gelesen.\n"
                         "Bitte die Spaltenüberschriften der Exceltabelle zuordnen, sodass das Programm diese einlesen "
                         "kann"
    },
    "page_select_xlsxfile_selecttext": {
        LANGUAGE_GERMAN: "Datei auswählen:"
    },
    "page_select_xlsxfile_browsebutton": {
        LANGUAGE_GERMAN: "Durchsuchen..."
    },
    "page_select_xlsxfile_col_url": {
        LANGUAGE_GERMAN: "Spalte Webseiten Links (URLs)"
    },
    "page_select_xlsxfile_testregistration": {
        LANGUAGE_GERMAN: "Teste Anmeldungen"
    },
    "page_testreg_headertext": {
        LANGUAGE_GERMAN: "Auf diese URL anwenden:"
    },
    "page_testreg_testcount": {
        LANGUAGE_GERMAN: "Testanzahl nach Status:"
    },
    "page_testreg_teacher": {
        LANGUAGE_GERMAN: "Lehrkraft:"
    },
    "page_testreg_students": {
        LANGUAGE_GERMAN: "Studierende*r:"
    },
    "page_testreg_teachingstudents": {
        LANGUAGE_GERMAN: "Lehramtsanwärter*in:"
    },
    "page_testreg_lkplus": {
        LANGUAGE_GERMAN: "Teilnehmer*in des Programms LehrkräftePlus:"
    },
    "page_testreg_other": {
        LANGUAGE_GERMAN: "Sonstige:"
    },
    "page_select_xlsxfile_popup_nofile": {
        LANGUAGE_GERMAN: "Es wurde keine Datei ausgewählt!"
    },
    "page_select_xlsxfile_popup_nourl": {
        LANGUAGE_GERMAN: "Es wurde keine Spalte für die URLs ausgewählt!"
    },
    "page_testreg_checkbox_randomnames": {
        LANGUAGE_GERMAN: "Zufällige Namen verwenden"
    },
    "page_testreg_name": {
        LANGUAGE_GERMAN: "Name:"
    },
    "page_testreg_prename": {
        LANGUAGE_GERMAN: "Vorname:"
    },
    "page_testreg_institution": {
        LANGUAGE_GERMAN: "Institution:"
    },
    "page_testreg_email": {
        LANGUAGE_GERMAN: "E-Mail:"
    },
    "page_testreg_start": {
        LANGUAGE_GERMAN: "Test starten"
    },
    "page_select_xlsxfile_testregerr": {
        LANGUAGE_GERMAN: "Teste Anmeldefehler"
    },
    "page_select_xlsxfile_testcontent": {
        LANGUAGE_GERMAN: "Teste Seiteninhalte"
    },
    "page_select_xlsxfile_popup_urlheaderwrong": {
        LANGUAGE_GERMAN: "Die Spaltenüberschrift für die URLs ist nicht in der Excel Tabelle zu finden!"
    }
}


def get_catalog_text(t):
    return CATALOG[t][LANGUAGE_USING]
