# Corona-Analysis-and-Prediction
This project is regarding corona virus analysis and prediction of number of cases in future.

### •   Corona Virus Analysis.

1.  COVID-19 disease hit in 2019 and in India 2020. So this project contains analysis of covid data.
2.	The project contains graphs, tables and prediction of cases in future.
	-	Graphs: Graphs will describe present situation of corona virus like confirmed cases and recovered cases.
	-	Tables: Tables contains past data, active data, today's data and rates.
3.	In analysis, it will describe testing statistics.
	-	Growth rate - ((((yesterdayConfirmedCases - 7DayBeforeConfirmedCase) / 7DayBeforeConfirmedCase) * 100) / 7).
	-	Population data - Indian States population data stored in file and stored in backend.
	-	Test per Million - (TotalTestsState * 1000000 / PopulationState)
	-	Confirm per Million - (TotalConfirmedCases * 1000000 / PopulationState)
4.	In prediction part, it will predict next 7 days data by analysing last 15 days.


### •   Step 1: Install All the dependencies.

1.  All the dependencies mentioned in requirements.txt
2.  Install using pip install -r requirements.txt

### •   Step 2: Run the application.

1.  Run covid.py which will run on http://127.0.0.1:65000.
2.  Visit this URL in web browser.

3.  If you want to run on specific IP then change "host" in covid.py
4.  And visit http://IP-ADDRESS:65000.
