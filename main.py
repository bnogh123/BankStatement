import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Grab and process the raw data.
    col = ["Status", "Month", "Day", "Description", "Debit", "Credit"]
    data_path = ("Files/CHK_0584_CURRENT_VIEW.csv")
    bank_raw = pd.read_csv(data_path, delimiter=',', names=col, index_col=False)
    pd.options.mode.chained_assignment = None

    for i in range(bank_raw["Description"].size):
        new = " "

        if bank_raw["Description"][i].startswith("Debit PIN Purchase"):
            new = bank_raw["Description"][i].replace("Debit PIN Purchase ", "")[:-22].strip()

        elif bank_raw["Description"][i].startswith("Debit Card Purchase"):
            new = bank_raw["Description"][i][38:-8].strip()

        elif bank_raw["Description"][i].startswith("Zelle"):
            new = "Zelle to " + bank_raw["Description"][i][48:].strip()

        elif bank_raw["Description"][i].startswith("Transfer"):
            new = "Transfer"

        if not new.isspace():
            bank_raw["Description"][i] = new

    small_purchases = bank_raw[(~bank_raw['Debit'].isnull()) & (bank_raw['Debit'] < 100.)]
    large_purchases = bank_raw[(~bank_raw['Debit'].isnull()) & (bank_raw['Debit'] >= 100.) & (bank_raw['Debit'] < 400.)]
    rent_else = bank_raw[(~bank_raw['Debit'].isnull()) & (bank_raw['Debit'] >= 100.) & (bank_raw['Debit'] >= 400.)]
    deposits = bank_raw[~bank_raw['Credit'].isnull()]

    small_purchases = small_purchases.loc[:, ["Month", "Day", "Description", "Debit"]]
    large_purchases = large_purchases.loc[:, ["Month", "Day", "Description", "Debit"]]
    rent_else = rent_else.loc[:, ["Month", "Day", "Description", "Debit"]]
    deposits = deposits.loc[:, ["Month", "Day", "Description", "Credit"]]

    # print(bank_raw)
    small_purchases.to_csv('Files/small_purchases.csv', index=False)
    large_purchases.to_csv('Files/large_purchases.csv', index=False)
    rent_else.to_csv('Files/rent_else.csv', index=False)
    deposits.to_csv('Files/deposits.csv', index=False)
