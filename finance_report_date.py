from datetime import datetime

import numpy as np
import pandas as pd


def process_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        try:
            return datetime.strptime(date_str, "%m/%d/%Y")
        except Exception as e:
            raise e
    except Exception as e:
        print(e)


def get_finance_report_date():
    df = pd.read_csv('raw/financeReportDate.csv')
    reports = {}
    for row in df.itertuples(index=False):
        symbol = row.Symbol
        dates = row.Date.split('|')
        dates = [process_date(date) for date in dates]
        dates.sort()
        reports[symbol] = dates
    return reports


finance_reports = get_finance_report_date()

def to_next_report_days(symbol, date_str):
    report_dates = finance_reports.get(symbol)
    if report_dates is None:
        return None
    date = datetime.strptime(date_str, "%Y-%m-%d")
    for report_date in report_dates:
        day_diff = (report_date - date).days
        if day_diff >= 0:
            return day_diff
    return None


def from_pass_report_days(symbol, date_str):
    report_dates = finance_reports.get(symbol)
    if report_dates is None:
        return None
    date = datetime.strptime(date_str, "%Y-%m-%d")
    for i in range(len(report_dates) - 1, -1, -1):
        report_date = report_dates[i]
        day_diff = (date - report_date).days - 1
        if day_diff >= 0:
            return day_diff
    return None

def merge_next_report_date():
    df = pd.read_csv('raw/OptionHistory.csv')
    next_report_days = df.apply(lambda row: to_next_report_days(row['ticker'], row['date']), axis=1)
    pass_report_days = df.apply(lambda row: from_pass_report_days(row['ticker'], row['date']), axis=1)
    df.insert(2, "next_report_days", next_report_days)
    df.insert(2, "pass_report_days", pass_report_days)
    df.to_csv("data/OptionHistory.csv", index=False)