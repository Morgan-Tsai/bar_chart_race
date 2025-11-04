import plotly.express as px
import pandas as pd
from create_bar_chart_race_data import CreateBarChartRaceData
from raceplotly.plots import barplot

#資料載入
create_bar_chart_race_data = CreateBarChartRaceData()
cumulative_votes_by_time_candidate = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()
covid_19_confirmed = create_bar_chart_race_data.create_covid_19_confirmed()
covid_19_deaths = create_bar_chart_race_data.create_covid_19_deaths()
covid_19_doses = create_bar_chart_race_data.create_covid_19_doses()


#投開票完成時間
early_collected = cumulative_votes_by_time_candidate[cumulative_votes_by_time_candidate["collected_at"] < pd.to_datetime("2024-01-13 20:50:00")]
#橫向長條圖
#item_column:y軸  value_column:x軸
vote_raceplot = barplot(early_collected,item_column="candidate",value_column="cumulative_sum_votes",
                        time_column="collected_at",top_entries=3)

#item_label:y軸標籤 value_label:x軸標籤
fig = vote_raceplot.plot(item_label="Votes collected by candidate",value_label="Cumulative votes",
                         frame_duration=50)

fig.update_layout(
    title="<b>2024年正副總統選舉 得票數變化</b><br>(資料來源:中選會選舉及公投資料庫)",
    title_font_size=25,
    title_x=0.5)   # 標題置中

fig.write_html("bar_chart_race_votes.html")

#covid 19 確診人數
#top_entries預設為10
confirmed_raceplot = barplot(covid_19_confirmed,item_column="country",value_column="confirmed",
                             time_column="reported_on")

fig = confirmed_raceplot.plot(item_label="Confirmed by country",value_label="Number of cases",frame_duration=50)

fig.update_layout(
    title="<b>2020年~2023年3月 Covid19全球診人數</b><br>(資料來源:CSSE at Johns Hopkins University)",
    title_font_size=30,
    title_x=0.5)

fig.write_html("bar_chart_race_confirmed.html")

#covid 19 死亡人數
deaths_raceplot = barplot(covid_19_deaths,item_column="country",value_column="deaths",
                          time_column="reported_on")

fig = deaths_raceplot.plot(item_label="Deaths by country",value_label="Number of cases",frame_duration=50)

fig.update_layout(
    title="<b>2020年~2023年3月 Covid19全球死亡人數</b><br>(資料來源:CSSE at Johns Hopkins University)",
    title_font_size=30,
    title_x=0.5)

fig.write_html("bar_chart_race_deaths.html")

#covid 19 疫苗施打人數
doses_raceplot = barplot(covid_19_doses,item_column="country",value_column="doses_administered",
                         time_column="reported_on")

fig = doses_raceplot.plot(item_label="Doses administered by country",value_label="Number of cases",frame_duration=50)

fig.update_layout(
    title="<b>2020年~2023年3月 Covid19全球疫苗施打人數</b><br>(資料來源:CSSE at Johns Hopkins University)",
    title_font_size=30,
    title_x=0.5)

fig.write_html("bar_chart_race_doses.html")
