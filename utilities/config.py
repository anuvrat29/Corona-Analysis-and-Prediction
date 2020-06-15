"""
    This configuration file contains all the constants.
"""
import os

INPUT = os.path.join(os.getcwd(), "utilities")
GRAPH_FOLDER = os.path.join(INPUT, "graph_folder")
INPUT_FOLDER = os.path.join(INPUT, "input_folder")
MANDATORY_FILES = os.path.join(INPUT, "mandatory_files")

COVID_URL = "https://covidstat.info/graphql"
QUERY = """ query {
                country(name: "India") {
                    states {
                        state
                        historical {
                            date
                            cases
                            deaths
                            recovered
                        }
                        todayCases
                        todayRecovered
                        todayDeaths
                    }
                }
            }
        """

CURRENT_QUERY = """ query {
                        country(name: "India") {
                        states {
                            state
                            tests
                            todayCases
                            todayRecovered
                            todayDeaths
                        }
                    }
                }
            """

FIGSIZE = (6, 4)
