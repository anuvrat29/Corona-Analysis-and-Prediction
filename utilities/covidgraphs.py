"""
    This python file will return all the basic graphs.
"""
# pylint: disable=R0914
# pylint: disable=E0401

import os
import shutil
from datetime import datetime

import requests
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
from utilities.config import GRAPH_FOLDER, FIGSIZE
from utilities.config import MANDATORY_FILES, COVID_URL, CURRENT_QUERY

POPULATION = pd.read_excel(os.path.join(MANDATORY_FILES, "population.xlsx"),\
                                                    sheet_name="population")

class COVIDGraphs:
    """
        This class contains methods for get covid graphs.
    """
    @classmethod
    def get_overall_graph(cls, date, confirm_df, recover_df, state):
        """
            This will return confirm case graph.
        """
        temp = 0
        confirm_cases = list()
        for value in confirm_df["date"].values:
            temp += sum(confirm_df[confirm_df["date"] == value][state])
            confirm_cases.append(temp)

        temp = 0
        recover_cases = list()
        for value in recover_df["date"].values:
            temp += sum(recover_df[recover_df["date"] == value][state])
            recover_cases.append(temp)

        mdate = [value[:-3] if index%7 == 0 else "" for index, value in enumerate(date)]

        with plt.rc_context({'axes.edgecolor': 'darkkhaki', 'xtick.color':'darkkhaki',\
                                                            'ytick.color':'darkkhaki'}):
            fig = plt.figure(figsize=FIGSIZE)
            axes = fig.add_subplot()
            axes.plot(date, confirm_cases, "r-", label="Confirmed")
            axes.plot(date, recover_cases, "g-", label="Recovered")
            plt.title("Confirmed and Recovered Cases Graph Over Time", color="darkkhaki")
            axes.yaxis.tick_right()
            plt.text(date[-1], confirm_cases[-1], f"{confirm_cases[-1]}",\
                                        horizontalalignment='center', color="aqua", fontsize=15)
            plt.text(date[-1], recover_cases[-1], f"{recover_cases[-1]}",\
                                        horizontalalignment='center', color="aqua", fontsize=15)
            plt.xticks(range(len(mdate)), mdate, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(GRAPH_FOLDER, "overall_graph.png"), transparent=True)
        return "overall_graph.png", confirm_cases[-7]

    @classmethod
    def get_overall_graph_daily(cls, date, confirm_df, recover_df, state):
        """
            This will return confirm case graph.
        """
        confirm_cases = list()
        for value in confirm_df["date"].values:
            confirm_cases.append(int(confirm_df[confirm_df["date"] == value][state]))

        recover_cases = list()
        for value in recover_df["date"].values:
            recover_cases.append(int(recover_df[recover_df["date"] == value][state]))

        mdate = [value[:-3] if index%7 == 0 else "" for index, value in enumerate(date)]

        with plt.rc_context({'axes.edgecolor': 'darkkhaki', 'xtick.color':'darkkhaki',\
                                                            'ytick.color':'darkkhaki'}):
            fig = plt.figure(figsize=FIGSIZE)
            axes = fig.add_subplot()
            axes.plot(date, confirm_cases, "r-", label="Confirmed")
            axes.plot(date, recover_cases, "g-", label="Recovered")
            plt.title("Confirmed and Recovered Cases Graph Daily Basis", color="darkkhaki")
            axes.yaxis.tick_right()
            plt.text(date[-1], confirm_cases[-1], f"{confirm_cases[-1]}",\
                                        horizontalalignment='center', color="aqua", fontsize=15)
            plt.text(date[-1], recover_cases[-1], f"{recover_cases[-1]}",\
                                        horizontalalignment='center', color="aqua", fontsize=15)
            plt.xticks(range(len(mdate)), mdate, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(GRAPH_FOLDER, "overall_graph_daily.png"), transparent=True)
        return "overall_graph_daily.png"

    @classmethod
    def get_death_graph(cls, date, death_df, state):
        """
            This will return death case graph.
        """
        temp = 0
        death_cases = list()
        for value in death_df["date"].values:
            temp += sum(death_df[death_df["date"] == value][state])
            death_cases.append(temp)

        death_cases_daily = list()
        for value in death_df["date"].values:
            death_cases_daily.append(int(death_df[death_df["date"] == value][state]))

        mdate = [value[:-3] if index%7 == 0 else "" for index, value in enumerate(date)]

        with plt.rc_context({'axes.edgecolor': 'darkkhaki', 'xtick.color':'darkkhaki',\
                                                            'ytick.color':'darkkhaki'}):
            fig = plt.figure(figsize=FIGSIZE)
            axes = fig.add_subplot()
            axes.plot(date, death_cases, color="#696969", label="Total Deaths")
            axes.plot(date, death_cases_daily, color="#2F4F4F", label="Daily Deaths")
            plt.title("Death Cases Graph Over Time", color="darkkhaki")
            axes.yaxis.tick_right()
            plt.text(date[-1], death_cases[-1], f"{death_cases[-1]}",\
                                horizontalalignment='center', color="aqua", fontsize=15)
            plt.text(date[-1], death_cases_daily[-1], f"{death_cases_daily[-1]}",\
                                horizontalalignment='center', color="aqua", fontsize=15)
            plt.xticks(range(len(mdate)), mdate, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(GRAPH_FOLDER, "death_graph.png"), transparent=True)
        return "death_graph.png"

    @classmethod
    def get_current_cases(cls, jsondata):
        """
            This method will return current cases data of mentioned particular states.
        """
        try:
            data = requests.post(COVID_URL, json={"query": CURRENT_QUERY}).json()
            for _, state in enumerate(data["data"]["country"]["states"]):
                if state["state"].lower() == jsondata["State"].lower():
                    test = None
                    if state["state"].lower() == "total":
                        test = sum([val["tests"]\
                                    for _, val in enumerate(data["data"]["country"]["states"])])
                    else:
                        test = state["tests"]
                    pop = int(POPULATION[POPULATION["State"] == jsondata["State"]]["Population"])
                    return {"new": state["todayCases"], "recovered": state["todayRecovered"],\
                            "dead": state["todayDeaths"], "tests": int(test), "population": pop}
        except requests.exceptions.ConnectionError:
            pass
        return {"new": 0, "recovered": 0, "dead": 0, "tests": 0, "population": 0}

    @classmethod
    def forecast_confirm_cases(cls, dataframe, jsondata):
        """
            This method will forecast the cases.
        """
        temp_int, temp_list, last_days = 0, list(), 15

        for _, value in enumerate(dataframe[jsondata["State"]]):
            temp_int = temp_int + value
            temp_list.append(temp_int)

        autoreg = AutoReg(temp_list[-15:], lags=1, trend="t")
        model = autoreg.fit()
        predicted_values = model.predict(last_days, last_days+6)
        predicted_values = [int(val) for val in predicted_values]
        last_date = list(dataframe["date"])[-1]
        date = [datetime.strptime(str(value).split()[0], '%Y-%m-%d').strftime("%d-%b")\
                        for value in pd.date_range(datetime.strptime(last_date, '%d-%b-%y'),\
                                                                periods=8).tolist()][1:]

        with plt.rc_context({'axes.edgecolor': 'darkkhaki', 'xtick.color':'darkkhaki',\
                                                            'ytick.color':'darkkhaki'}):
            fig = model.plot_predict(last_days, last_days+6, alpha=0.05, figsize=FIGSIZE)
            plt.plot(range(7), predicted_values, "ro")
            axes = fig.add_subplot()
            plt.title("Confirm Case Forecasting", color="darkkhaki")
            axes.yaxis.tick_right()
            for index, value in enumerate(predicted_values):
                axes.text(index, value, f"{value}",\
                                horizontalalignment='center', color="aqua", fontsize=12)
            plt.xticks(range(len(date)), date, size='small')
            plt.savefig(os.path.join(GRAPH_FOLDER, "forecasted_graph.png"), transparent=True)
        return "forecasted_graph.png"

    @classmethod
    def run_covidgraphs(cls, jsondata, confirm_df, recover_df, death_df):
        """
            This will return all the graphs.
        """
        result = dict()

        if not os.path.isdir(GRAPH_FOLDER):
            os.mkdir(GRAPH_FOLDER)
        else:
            shutil.rmtree(GRAPH_FOLDER)
            os.mkdir(GRAPH_FOLDER)

        overall = cls.get_overall_graph(list(confirm_df["date"]), confirm_df,\
                                        recover_df, jsondata["State"])
        overall_daily = cls.get_overall_graph_daily(list(confirm_df["date"]), confirm_df,\
                                        recover_df, jsondata["State"])
        dead = cls.get_death_graph(list(death_df["date"]), death_df, jsondata["State"])
        forecast_graph = cls.forecast_confirm_cases(confirm_df, jsondata)

        result["overall_graph"] = overall[0]
        result["death_graph"] = dead
        result["overall_daily"] = overall_daily
        result["forecasted_graph"] = forecast_graph

        result["todaystats"] = cls.get_current_cases(jsondata)
        result["confirmed"] = sum(confirm_df[jsondata["State"]])
        result["recovered"] = sum(recover_df[jsondata["State"]])
        result["dead"] = sum(death_df[jsondata["State"]])
        result["rate_case"] = int(overall[1])

        return result
