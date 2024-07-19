import pandas as pd
import matplotlib.pyplot as plt
from process_data import MatchHistory
from web.statsgraph_web.statgraphs.api_request import *

class CreatePlt:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def winrate_per_day_plot(self) -> plt.Figure:
        match_history = MatchHistory(self.df)
        match_history.get_match_day("gameCreation")
        filtered_history = match_history.filter_by_win()
        victories_by_day = filtered_history['gameCreation'].value_counts()

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        victories_by_day = victories_by_day.reindex(days_of_week, fill_value=0)

        total_victories = victories_by_day.sum()

        if total_victories > 0:
            win_rate_by_day = (victories_by_day / total_victories) * 100
        else:
            win_rate_by_day = pd.Series([0]*7, index=days_of_week)

        fig, ax = plt.subplots()
        win_rate_by_day.plot(kind='bar', ax=ax)
        ax.set_xlabel('Día de la semana')
        ax.set_ylabel('Porcentaje de victorias')
        ax.set_title('Tasa de victorias según el día de la semana')
        plt.show()

        return fig

    def winrate_per_hour_plot(self) -> plt.Figure:
        match_history = MatchHistory(self.df)
        match_history.get_match_hour("gameCreation")
        filtered_history = match_history.filter_by_win()
        victories_by_hour = filtered_history['gameCreation'].value_counts()
        all_hours = pd.Series(0, index=range(24))
        victories_by_hour = all_hours.add(victories_by_hour, fill_value=0)
        total_victories = victories_by_hour.sum()
        if total_victories > 0:
            win_rate_by_hour = round((victories_by_hour / total_victories) * 100)
        else:
            win_rate_by_hour = 0 

        fig, ax = plt.subplots()
        win_rate_by_hour.plot(kind='bar', ax=ax)
        ax.set_xlabel('Hora')
        ax.set_ylabel('Porcentaje de victorias')
        ax.set_title('Tasa de victorias según la hora del día')
        ax.set_xticks([0, 5, 10, 15, 20])
        ax.set_xticklabels([0, 5, 10, 15, 20])
        plt.show()

        return fig

if __name__ == "__main__":
    api_request_app = StatsApp()

    region = "americas"
    game_name  = input("Mandate el game name: ")
    tag_line = input("Mandate el tag line: ").upper()
    puuid = api_request_app.get_player_puuid(region, game_name, tag_line)
    matches_list = api_request_app.get_matches_list(region, puuid)
    dictionary = api_request_app.get_every_match_data(region, matches_list, puuid)

    df = pd.DataFrame.from_dict(dictionary, orient="index")
    match_history = MatchHistory(df)

    print(match_history.get_kda())
    # plot_creator = CreatePlt(df)
    # plot_creator.winrate_per_hour_plot()
