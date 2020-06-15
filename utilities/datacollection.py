"""
    This file contains all the collection data methods.
"""
# pylint: disable=R0914
# pylint: disable=E0110

import os
from datetime import datetime

import requests
import pandas as pd
from utilities.config import QUERY, COVID_URL, INPUT_FOLDER

class DataCollection:
    """
        This class contains all the methods of data collection.
    """
    @classmethod
    def read_excel(cls, file):
        """
            This method will read file and return dataframes.
        """
        confirm_df = pd.read_excel(file, sheet_name="confirm_data")
        recover_df = pd.read_excel(file, sheet_name="recover_data")
        death_df = pd.read_excel(file, sheet_name="death_data")
        return confirm_df, recover_df, death_df

    @classmethod
    def read_data_from_url(cls, jsondata):
        """
            This method will read data from URL and return dataframes.
        """
        date, confirm_dict, recover_dict, death_dict = list(), dict(), dict(), dict()
        confirm_df, recover_df, death_df = None, None, None

        data = requests.post(COVID_URL, json={"query": QUERY}).json()
        for _, state in enumerate(data["data"]["country"]["states"]):

            confirmed, recovered, deceased = 0, 0, 0
            if state["state"] == "State Unassigned":
                continue
            if state["state"] == "Total":
                for _, historical in enumerate(state["historical"]):
                    date.append(str(datetime.strptime(historical["date"].replace("/", "-"),\
                                                            '%m-%d-%y').strftime("%d-%b-%y")))

            confirm, recover, death = list(), list(), list()
            for _, historical in enumerate(state["historical"]):
                confirmed = historical["cases"] - confirmed
                confirm.append(confirmed)
                confirmed = historical["cases"]
                recovered = historical["recovered"] - recovered
                recover.append(recovered)
                recovered = historical["recovered"]
                deceased = historical["deaths"] - deceased
                death.append(deceased)
                deceased = historical["deaths"]

            confirm_dict["date"] = date
            confirm_dict[state["state"]] = confirm
            recover_dict["date"] = date
            recover_dict[state["state"]] = recover
            death_dict["date"] = date
            death_dict[state["state"]] = death

        confirm_df = pd.DataFrame(confirm_dict)
        recover_df = pd.DataFrame(recover_dict)
        death_df = pd.DataFrame(death_dict)

        writer = pd.ExcelWriter(os.path.join(INPUT_FOLDER, f"{jsondata['Date']}.xlsx"),\
                                                                        engine="openpyxl")
        confirm_df.to_excel(writer, sheet_name="confirm_data", index=False)
        recover_df.to_excel(writer, sheet_name="recover_data", index=False)
        death_df.to_excel(writer, sheet_name="death_data", index=False)
        writer.save()

        return confirm_df, recover_df, death_df

    @classmethod
    def get_data(cls, jsondata):
        """
            Get historical covid data using URL.
        """
        if not os.path.isdir(INPUT_FOLDER):
            os.mkdir(INPUT_FOLDER)

        confirm_df, recover_df, death_df = None, None, None
        file = None

        if os.path.isfile(os.path.join(INPUT_FOLDER, f"{jsondata['Filename']}.xlsx")):
            file = os.path.join(INPUT_FOLDER, f"{jsondata['Filename']}.xlsx")
            confirm_df, recover_df, death_df = cls.read_excel(file)
        else:
            confirm_df, recover_df, death_df = cls.read_data_from_url(jsondata)

        return confirm_df, recover_df, death_df
