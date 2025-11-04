import sqlite3
import pandas as pd

class CreateBarChartRaceData:
#日期時間格式轉換
    def adjust_datetime_format(self,x:str):
        date_part,time_part = x.split()
        date_part = "2024-01-13"
        datetime_iso_8601 = f"{date_part} {time_part}"
        return datetime_iso_8601

    def create_cumulative_votes_by_time_candidate(self):
        #選舉資料建立
        connection = sqlite3.connect("data/taiwan_election_2024.db")
        sql_query = """
        SELECT p.county,p.polling_place,c.candidate,SUM(v.votes) AS sum_votes
        FROM votes v
        JOIN candidates c
            on  v.candidate_id = c.id
        JOIN polling_places p
            on v.polling_place_id = p.id
        GROUP BY p.county,p.polling_place,c.candidate;
        """
        votes_by_county_polling_place_candidate = pd.read_sql(sql_query,con=connection)
        connection.close()

        votes_collected = pd.read_excel("data/113全國投開票所完成時間.xlsx",skiprows=[0,1,2])
        votes_collected.columns = ["county","town","polling_place","collected_at","number_of_voters"]
        votes_collected = votes_collected[["county","town","polling_place","collected_at"]]

        merged = pd.merge(votes_by_county_polling_place_candidate,votes_collected,
                        left_on=["county","polling_place"],right_on=["county","polling_place"],how="left")
        votes_by_collected_at_candidate =merged.groupby(["collected_at","candidate"])["sum_votes"].sum().reset_index()

        cum_sum = votes_by_collected_at_candidate.groupby("candidate")["sum_votes"].cumsum()
        votes_by_collected_at_candidate["cumulative_sum_votes"] = cum_sum
        votes_by_collected_at_candidate["collected_at"] = votes_by_collected_at_candidate["collected_at"].map(self.adjust_datetime_format)
        votes_by_collected_at_candidate["collected_at"] = pd.to_datetime(votes_by_collected_at_candidate["collected_at"])
        return votes_by_collected_at_candidate
    
    def create_covid_19_confirmed(self):
        #疫情資料建立
        connection = sqlite3.connect("data/covid_19.db")
        sql_query_confirmed = """
        SELECT reported_on,country,confirmed
          FROM time_series;
        """
        covid_19_confirmed = pd.read_sql(sql_query_confirmed,con=connection)
        connection.close()

        nlargest_index_confirmed = covid_19_confirmed.groupby("reported_on")["confirmed"].nlargest(10).reset_index()["level_1"]
        covid_19_confirmed = covid_19_confirmed.loc[nlargest_index_confirmed,:].reset_index(drop=True)
        return covid_19_confirmed
    
    def create_covid_19_deaths(self):
        connection = sqlite3.connect("data/covid_19.db")
        sql_query_deaths = """
        SELECT reported_on,country,deaths
        FROM time_series;
        """
        covid_19_deaths = pd.read_sql(sql_query_deaths,con=connection)
        connection.close()

        nlargest_index_deaths = covid_19_deaths.groupby("reported_on")["deaths"].nlargest(10).reset_index()["level_1"]
        covid_19_deaths = covid_19_deaths.loc[nlargest_index_deaths,:].reset_index(drop=True)
        return covid_19_deaths
    
    def create_covid_19_doses(self):
        connection = sqlite3.connect("data/covid_19.db")
        sql_query_doses = """
        SELECT reported_on,country,doses_administered
        FROM time_series;
        """
        covid_19_doses = pd.read_sql(sql_query_doses,con=connection)
        connection.close()

        nlargest_index_doses = covid_19_doses.groupby("reported_on")["doses_administered"].nlargest(10).reset_index()["level_1"]
        covid_19_doses = covid_19_doses.loc[nlargest_index_doses,:].reset_index(drop=True)
        return covid_19_doses
