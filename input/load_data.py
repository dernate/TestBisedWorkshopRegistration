#!/usr/bin/env python3
import pandas as pd


def xlsx_load(fn: str) -> pd.DataFrame:
    return pd.read_excel(fn)


def xlsx_get_columns(fn) -> list:
    df = xlsx_load(fn)
    return df.columns


def xlsx_get_urls(fn: str, column_name: str) -> list:
    df = xlsx_load(fn)
    return df[column_name].tolist()
